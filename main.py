from fastapi import FastAPI
import uvicorn
from app.routes.genre import app as genreapi
from contextlib import asynccontextmanager
from app.database import Base , engine


@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(engine)
    yield
    #after...

app = FastAPI(lifespan=lifespan)

app.include_router(genreapi)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",   
        host="0.0.0.0",
        port=8080,
        reload=True
    )