from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Form

class ItemModel(BaseModel):
    id: Optional[str] = None
    name: str
    description: str

    @classmethod
    def from_form(cls, name: str = Form(...), description: str = Form(...)):
        return cls(name=name, description=description)