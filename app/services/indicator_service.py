from ..repositories.indicator_repository import IndicatorRepository
from ..models.indicator_model import IndicatorModel
from typing import List, Optional

class IndicatorService:
    def __init__(self, repository: IndicatorRepository = None):
        self.repository = repository or IndicatorRepository()

    async def create_indicator(self, indicator: IndicatorModel) -> str:
        result = await self.repository.create(indicator)
        await self.update_indonesia_average(indicator.title, indicator.year)
        return result
    
    async def get_indicators(self) -> List[IndicatorModel]:
        return await self.repository.get_all()
    
    async def get_unique_provinces(self) -> List[str]:
        return await self.repository.get_unique_provinces()
    
    async def get_unique_title(self) -> List[str]:
        return await self.repository.get_unique_title()
    
    async def get_unique_year_based_on_title(self, title: str) -> List[int]:
        return await self.repository.get_unique_year_based_on_title(title)
    
    async def get_by_province(self, province: str) -> List[IndicatorModel]:
        return await self.repository.get_by_province(province)
    
    async def get_by_title_and_year(self, title: str, year: int) -> List[IndicatorModel]:
        return await self.repository.get_by_title_and_year(title, year)
    
    async def get_unique_title_by_indicator(self, indicator: str) -> List[str]:
        return await self.repository.get_unique_title_by_indicator(indicator)
    
    async def filter_indicators(
        self,
        province: Optional[str] = None,
        title: Optional[str] = None,
        indicator: Optional[str] = None,
        year_range: Optional[str] = None
    ) -> List[IndicatorModel]:
        return await self.repository.filter(province, title, indicator, year_range)
    
    async def get_unique_indicator(self) -> List[str]:
        return await self.repository.get_unique_indicator()

    async def get_indicator_by_id(self, indicator_id: str) -> IndicatorModel:
        return await self.repository.get_by_id(indicator_id)

    async def update_indicator(self, indicator: IndicatorModel) -> None:
        await self.repository.update(indicator)

    async def delete_indicator(self, indicator_id: str) -> None:
        await self.repository.delete(indicator_id)

    async def get_by_title_and_province(self, title: str, province: str) -> List[IndicatorModel]:
        return await self.repository.get_by_title_and_province(title, province)

    async def update_indonesia_average(self, title: str, year: int) -> None:
        await self.repository.update_indonesia_average(title, year)

    async def get_national_average(self, title: str, year: int) -> Optional[IndicatorModel]:
        return await self.repository.get_national_average(title, year)


def get_indicator_service():
    return IndicatorService()