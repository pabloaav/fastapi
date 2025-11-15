from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class MovieCreateDTO(BaseModel):
    title: str
    overview: str = Field(min_length=10, max_length=255)
    year: int = Field(gt=1900, le=datetime.now().year)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=3, max_length=20)
    model_config = {
        'json_schema_extra': {
            'example': {
                "title": "Inception",
                "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                "year": 2010,
                "rating": 8.8,
                "category": "Sci-Fi"
            }
        }
    }

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty_or_only_spaces(cls, v):
        if not v or v.isspace():
            raise ValueError(
                'El título no puede estar vacío o contener solo espacios')
        tiene_letra = False
        for char in v:
            if char.isalpha():
                tiene_letra = True
                break
        if not tiene_letra:
            raise ValueError('El título debe contener al menos una letra')
        return v.strip().title()


class MovieUpdateDTO(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


class MovieResponseDTO(BaseModel):
    id: Optional[int]
    title: str
    overview: str
    year: int
    rating: float
    category: str
