from typing import List, Optional
from src.domain.movie.movie_entity import MovieEntity


class MovieService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_movies(self) -> List[MovieEntity]:
        return self.repository.get_all()

    def get_movie_by_id(self, id: int) -> Optional[MovieEntity]:
        return self.repository.get_by_id(id)

    def get_movies_by_category(self, category: str) -> List[MovieEntity]:
        return self.repository.get_by_category(category)

    def create_movie(self, movie: MovieEntity) -> MovieEntity:
        return self.repository.create(movie)

    def update_movie(self, id: int, movie: MovieEntity) -> Optional[MovieEntity]:
        return self.repository.update(id, movie)

    def delete_movie(self, id: int) -> Optional[MovieEntity]:
        return self.repository.delete(id)
