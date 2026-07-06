from pydantic import BaseModel , PositiveFloat

class BaseGenre(BaseModel):
    name:str
class BaseDirector(BaseModel):
    fullname:str

class BaseMovieSchema(BaseModel):
    title : str
    description:str
    release_year : int
    genre :list[BaseGenre]
    director :BaseDirector
    imdb_rating : PositiveFloat

    

class CreateGenre(BaseGenre):
    pass
class CreateDirector(BaseDirector):
    pass
class CreateMovie(BaseMovieSchema):
    pass
