from fastapi import FastAPI
import uvicorn
from app.routes.genre import app as genreapi
from app.routes.director import app as directorapi
from app.routes.movie import app as movieapi
from contextlib import asynccontextmanager
from app.database import Base , engine


@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(engine)
    yield
    #after...

app = FastAPI(lifespan=lifespan)

app.include_router(genreapi)
app.include_router(directorapi)
app.include_router(movieapi)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",   
        host="0.0.0.0",
        port=8080,
        reload=True
    )