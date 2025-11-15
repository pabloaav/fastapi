from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse, RedirectResponse
from typing import List
from src.controllers.schemas import MovieCreateDTO, MovieUpdateDTO, MovieResponseDTO
from src.services.movie_service import MovieService
from src.repositories.movie_repository import MovieRepository
from src.domain.entities import MovieEntity

router = APIRouter(prefix="/movies", tags=["movies"])

# Instanciar repositorio y servicio
repository = MovieRepository()
service = MovieService(repository)


@router.get("", response_model=List[MovieResponseDTO])
def get_movies() -> JSONResponse:
    movies = service.get_all_movies()
    contenido = {
        "status": "success",
        "data": [movie.to_dict() for movie in movies],
        "total": len(movies)
    }
    return JSONResponse(status_code=200, content=contenido)


@router.get("/{id}", response_model=MovieResponseDTO)
def get_movie(
    id: int = Path(ge=1, le=1000, title="The ID of the movie to get",
                   description="Must be between 1 and 1000")
):
    movie = service.get_movie_by_id(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    contenido = {
        "status": "success",
        "data": movie.to_dict()
    }
    return JSONResponse(status_code=200, content=contenido)


@router.get("/category/{category}")
def get_movie_by_category(
    category: str = Path(
        ...,
        min_length=3,
        max_length=20,
        regex=r"^[A-Za-z0-9 \-]+$",
        description="Nombre de la categoría (3-20 caracteres). Letras, números, espacios y guiones permitidos.",
        title="Category name",
    )
):
    movies = service.get_movies_by_category(category)
    if not movies:
        raise HTTPException(
            status_code=404, detail=f"No movies found in category: {category}")
    contenido = {
        "status": "success",
        "data": [movie.to_dict() for movie in movies],
        "total": len(movies)
    }
    return JSONResponse(status_code=200, content=contenido)


@router.post("", status_code=201)
def create_movie(movie_dto: MovieCreateDTO):
    movie = MovieEntity(None, movie_dto.title, movie_dto.overview,
                        movie_dto.year, movie_dto.rating, movie_dto.category)
    service.create_movie(movie)
    return RedirectResponse(url="/movies", status_code=303)


@router.put("/{id}")
def update_movie(id: int, movie_dto: MovieUpdateDTO) -> JSONResponse:
    movie = MovieEntity(id, movie_dto.title, movie_dto.overview,
                        movie_dto.year, movie_dto.rating, movie_dto.category)
    updated = service.update_movie(id, movie)
    if not updated:
        raise HTTPException(
            status_code=404, detail=f"Movie with id {id} not found")
    contenido = {
        "status": "success",
        "data": updated.to_dict(),
        "message": "Movie updated successfully"
    }
    return JSONResponse(status_code=200, content=contenido)


@router.delete("/{id}")
def delete_movie(id: int) -> JSONResponse:
    deleted = service.delete_movie(id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail=f"Movie with id {id} not found")
    contenido = {
        "status": "success",
        "data": deleted.to_dict(),
        "message": "Movie deleted successfully"
    }
    return JSONResponse(status_code=200, content=contenido)


@router.get("/test/error")
def test_error():
    """Endpoint de prueba que lanza ValueError"""
    raise ValueError("Este es un error de prueba del middleware")


@router.get("/test/generic-error")
def test_generic_error():
    """Endpoint de prueba que lanza excepción genérica"""
    raise RuntimeError("Error genérico de prueba")
