from typing import List, Optional
from src.domain.entities import MovieEntity


class MovieRepository:
    def __init__(self):
        # Simulamos base de datos en memoria
        self.movies: List[MovieEntity] = [
            MovieEntity(1, "Movie 1", "Overview 1", 2020, 7.5, "Action"),
            MovieEntity(2, "Movie 2", "Overview 2", 2019, 8.0, "Comedy"),
            MovieEntity(3, "Movie 3", "Overview 3", 2021, 6.5, "Drama"),
        ]

    def get_all(self) -> List[MovieEntity]:
        return self.movies

    def get_by_id(self, id: int) -> Optional[MovieEntity]:
        for movie in self.movies:
            if movie.id == id:
                return movie
        return None

    def get_by_category(self, category: str) -> List[MovieEntity]:
        return [m for m in self.movies if m.category.lower() == category.lower()]

    def create(self, movie: MovieEntity) -> MovieEntity:
        new_id = max((m.id or 0 for m in self.movies), default=0) + 1
        movie.id = new_id
        self.movies.append(movie)
        return movie

    def update(self, id: int, movie: MovieEntity) -> Optional[MovieEntity]:
        for index, m in enumerate(self.movies):
            if m.id == id:
                movie.id = id
                self.movies[index] = movie
                return movie
        return None

    def delete(self, id: int) -> Optional[MovieEntity]:
        for index, m in enumerate(self.movies):
            if m.id == id:
                return self.movies.pop(index)
        return None
