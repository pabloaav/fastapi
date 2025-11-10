from datetime import datetime
from fastapi import FastAPI, Body, HTTPException, Path, Query
# importar respuestas para html
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# app title
app.title = "Probando FastAPI"
app.version = "0.0.1"


class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    overview: str
    year: int
    rating: float
    category: str


class MovieCreate(BaseModel):
    title: str = Field(min_length=5, max_length=25)
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


class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


# Lista de movies
movies = [
    Movie(id=1, title="Movie 1", overview="Overview 1",
          year=2020, rating=7.5, category="Action"),
    Movie(id=2, title="Movie 2", overview="Overview 2",
          year=2019, rating=8.0, category="Comedy"),
    Movie(id=3, title="Movie 3", overview="Overview 3",
          year=2021, rating=6.5, category="Drama"),
]


# Crear primera ruta basica


@app.get("/", tags=["home"])
def home():
    return {"message": "Esto es Python!!, Bienvenido a fastapi!"}

# Return a list of movies


@app.get("/movies", tags=["movies"])
def get_movies():
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": [movie.model_dump() for movie in movies],
            "total": len(movies)
        }
    )


# get only one movie by id


@app.get("/movies/{id}", tags=["movies"])
def get_movie(
    id: int = Path(ge=1, le=1000, title="The ID of the movie to get",
                   description="Must be between 1 and 1000")
) -> Movie:
    for movie in movies:
        if movie.id == id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

# get movie by query parameter category


@app.get("/movies/", tags=["movies"])
def get_movie_by_category(
    category: str = Query(
        ...,
        min_length=3,
        max_length=20,
        regex=r"^[A-Za-z0-9 \-]+$",
        description="Nombre de la categoría (3-20 caracteres). Letras, números, espacios y guiones permitidos.",
        title="Category name",
    )
) -> List[Movie]:
    movies_by_category: List[Movie] = []
    for movie in movies:
        if movie.category.lower() == category.lower():
            movies_by_category.append(movie)
    if not movies_by_category:
        raise HTTPException(
            status_code=404, detail=f"No movies found in category: {category}")
    return movies_by_category

# create movie whit post method


@app.post("/movies", tags=["movies"], status_code=201)
def create_movie(movie: MovieCreate) -> Movie:
    # Crear un nuevo Movie y asignar un nuevo ID
    # Expresion generadora para obtener el maximo id actual: (m.id or 0 for m in movies)
    new_id = max((m.id or 0 for m in movies), default=0) + 1
    new_movie = Movie(id=new_id, **movie.model_dump())
    movies.append(new_movie)
    return new_movie

# put method for movie


@app.put("/movies/{id}", tags=["movies"])
def update_movie(id: int, movie: MovieUpdate) -> Movie:
    for index, m in enumerate(movies):
        if m.id == id:
            # Crear un nuevo Movie con los datos actualizados
            updated_movie = Movie(id=id, **movie.model_dump())
            movies[index] = updated_movie
            return updated_movie
    raise HTTPException(
        status_code=404, detail=f"Movie with id {id} not found")

# delete method for movie


@app.delete("/movies/{id}", tags=["movies"], status_code=204)
def delete_movie(id: int):
    for index, m in enumerate(movies):
        if m.id == id:
            del movies[index]
            return None
    raise HTTPException(
        status_code=404, detail=f"Movie with id {id} not found")
