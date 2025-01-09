from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Form


class IndicatorModel(BaseModel):
    id: Optional[str] = None
    province: str
    year: int
    title: str
    indicator: str
    value: float

    @classmethod
    def from_form(cls, province: str = Form(...), year: int = Form(...), title: str = Form(...), indicator: str = Form(...), value: float = Form(...)):
        return cls(province=province, year=year, title=title, indicator=indicator, value=value)