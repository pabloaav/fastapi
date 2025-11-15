from typing import Optional


class MovieEntity:
    def __init__(
        self,
        id: Optional[int],
        title: str,
        overview: str,
        year: int,
        rating: float,
        category: str
    ):
        self.id = id
        self.title = title
        self.overview = overview
        self.year = year
        self.rating = rating
        self.category = category

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "overview": self.overview,
            "year": self.year,
            "rating": self.rating,
            "category": self.category
        }
