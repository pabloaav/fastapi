from fastapi import FastAPI
from fastapi.responses import FileResponse
from src.infrastructure.api.routes.movie_routes import router as movie_router

app = FastAPI()

# app title
app.title = "Probando FastAPI"
app.version = "0.0.1"


@app.get("/", tags=["home"])
def home():
    return {"message": "Esto es Python!!, Bienvenido a fastapi!"}


# Incluir routers
app.include_router(movie_router)
