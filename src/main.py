from fastapi import FastAPI
from src.controllers.movie_controller import router as movie_router
from src.infrastructure.middleware.error_handler import ErrorHandlerMiddleware

app = FastAPI()

# Aplicar middleware de manejo de errores
app.add_middleware(ErrorHandlerMiddleware)

app.title = "Probando FastAPI"
app.version = "0.0.1"


@app.get("/", tags=["home"])
def home():
    return {"message": "Bienvenido a la API FastAPI"}


# Incluir routers
app.include_router(movie_router)
