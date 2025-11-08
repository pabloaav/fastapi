from fastapi import FastAPI
# importar respuestas para html
from fastapi.responses import HTMLResponse

app = FastAPI()

# app title
app.title = "Probando FastAPI"
app.version = "0.0.1"
# Lista de movies
movies = [
    {"id": 1, "title": "Movie 1", "overview": "Overview 1",
        "year": 2020, "rating": 7.5, "category": "Action"},
    {"id": 2, "title": "Movie 2", "overview": "Overview 2",
        "year": 2019, "rating": 8.0, "category": "Comedy"},
    {"id": 3, "title": "Movie 3", "overview": "Overview 3",
        "year": 2021, "rating": 6.5, "category": "Drama"},
]


# Crear primera ruta basica


@app.get("/", tags=["home"])
def home():
    return {"message": "Esto es Python!!, Bienvenido a fastapi!"}

# una ruta para movies


@app.get("/movies", tags=["movies"])
def get_movies():

    return {"movies": movies}

# get only one movie by id


@app.get("/movies/{id}", tags=["movies"])
def get_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            return movie
    return {"message": "Movie not found"}

# get movie by query parameter category


@app.get("/movies/", tags=["movies"])
def get_movie_by_category(category: str):
    movies_by_category = []
    for movie in movies:
        if movie["category"].lower() == category.lower():
            movies_by_category.append(movie)
    return {"movies": movies_by_category}
