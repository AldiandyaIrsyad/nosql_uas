from ..core.database import Database
from ..models.indicator_model import IndicatorModel

from typing import List, Optional
from bson import ObjectId

class IndicatorRepository:
    def __init__(self, database=None):
        self.db = database or Database.get_db()
        self.collection = self.db["indicators"]

    async def create(self, indicator: IndicatorModel) -> str:
        result = await self.collection.insert_one(indicator.model_dump(exclude={"id"}))
        
        # Update the indonesia average after creating a new indicator
        await self.update_indonesia_average(indicator.title, indicator.year)
        
        return str(result.inserted_id)

    async def get_all(self) -> List[IndicatorModel]:
        pipeline = [
            {"$addFields": {"id": {"$toString": "$_id"}}},
            {"$project": {"_id": 0}}
        ]
        cursor = self.collection.aggregate(pipeline)
        documents = await cursor.to_list(length=None)
        return [IndicatorModel(**doc) for doc in documents]
    
    # get al by title and year
    async def get_by_title_and_year(self, title: str, year: int) -> List[IndicatorModel]:
        pipeline = [
            {"$match": {"title": title, "year": year}},
            {"$addFields": {"id": {"$toString": "$_id"}}},
            {"$project": {"_id": 0}}
        ]
        cursor = self.collection.aggregate(pipeline)
        documents = await cursor.to_list(length=None)
        return [IndicatorModel(**doc) for doc in documents]
    
    async def get_unique_provinces(self) -> List[str]:
        cursor = await self.collection.distinct("province")
        return cursor
    
    
    async def get_by_province(self, province: str) -> List[IndicatorModel]:
        pipeline = [
            {"$match": {"province": province}},
            {"$addFields": {"id": {"$toString": "$_id"}}},
            {"$project": {"_id": 0}}
        ]
        cursor = self.collection.aggregate(pipeline)
        documents = await cursor.to_list(length=None)
        return [IndicatorModel(**doc) for doc in documents]
    
    async def get_unique_title(self) -> List[str]:
        cursor = await self.collection.distinct("title")
        return cursor
    
    async def get_unique_year_based_on_title(self, title: str) -> List[int]:
        cursor = await self.collection.distinct("year", {"title": title})
        return sorted(cursor, reverse=True)

    async def filter(
        self,
        province: Optional[str] = None,
        title: Optional[str] = None,
        indicator: Optional[str] = None,
        year_range: Optional[str] = None
    ) -> List[IndicatorModel]:
        query = {}
        if province:
            query["province"] = province
        if title:
            query["title"] = title
        if indicator:
            query["indicator"] = indicator
        if year_range:
            years = year_range.split('-')
            if len(years) == 1:
                start_year = end_year = int(years[0])
            else:
                start_year, end_year = map(int, years)
            query["year"] = {"$gte": start_year, "$lte": end_year}
        
        pipeline = [
            {"$match": query},
            {"$addFields": {"id": {"$toString": "$_id"}}},
            {"$project": {"_id": 0}}
        ]
        cursor = self.collection.aggregate(pipeline)
        documents = await cursor.to_list(length=None)
        
        indicators = []
        for doc in documents:
            if all(key in doc for key in ["province", "year", "title", "indicator", "value"]):
                indicators.append(IndicatorModel(**doc))
            else:
                print(f"Invalid indicator: {doc}")
        
        return indicators

    async def get_unique_title_by_indicator(self, indicator: str) -> List[str]:
        cursor = await self.collection.distinct("title", {"indicator": indicator})
        return cursor
    
    async def get_unique_indicator(self) -> List[str]:
        cursor = await self.collection.distinct("indicator")
        return cursor

    async def get_by_id(self, indicator_id: str) -> IndicatorModel:
        document = await self.collection.find_one({"_id": ObjectId(indicator_id)})
        if document:
            document["id"] = str(document.pop("_id"))
            return IndicatorModel(**document)
        return None

    async def update(self, indicator: IndicatorModel) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(indicator.id)},
            {"$set": indicator.model_dump(exclude={"id"})}
        )

    async def delete(self, indicator_id: str) -> None:
        await self.collection.delete_one({"_id": ObjectId(indicator_id)})

    async def get_by_title_and_province(self, title: str, province: str) -> List[IndicatorModel]:
        pipeline = [
            {"$match": {"title": title, "province": province}},
            {"$addFields": {"id": {"$toString": "$_id"}}},
            {"$project": {"_id": 0}}
        ]
        cursor = self.collection.aggregate(pipeline)
        documents = await cursor.to_list(length=None)
        return [IndicatorModel(**doc) for doc in documents]

    async def update_indonesia_average(self, title: str, year: int) -> None:
        cursor = self.collection.find({"title": title, "year": year, "province": {"$ne": "indonesia"}})
        
        values = []
        indicator = ""
        async for document in cursor:

            values.append(document["value"])
            indicator = document["indicator"]

        if values:
            average_value = sum(values) / len(values)
        else:
            average_value = 0  


        await self.collection.update_one(
            {"title": title, "year": year, "province": "indonesia", "indicator": indicator},
            {"$set": {"value": average_value}},
            upsert=True
        )


    async def get_national_average(self, title: str, year: int) -> Optional[IndicatorModel]:
        document = await self.collection.find_one({"title": title, "year": year, "province": "indonesia"})
        if document:
            document["id"] = str(document.pop("_id"))
            # Ensure all required fields are present
            if "province" in document and "year" in document and "title" in document and "indicator" in document and "value" in document:
                return IndicatorModel(**document)
        return None