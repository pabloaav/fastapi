from fastapi import FastAPI
from src.controllers.movie_controller import router as movie_router

app = FastAPI()

app.title = "Probando FastAPI"
app.version = "0.0.1"


@app.get("/", tags=["home"])
def home():
    return {"message": "Bienvenido a la API FastAPI"}


# Incluir routers
app.include_router(movie_router)
