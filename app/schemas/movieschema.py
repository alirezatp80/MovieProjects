from pydantic import BaseModel ,ConfigDict
from app.schemas.genreschema import BaseGenre
from app.schemas.directorschema import BaseDirector

class BaseMovie(BaseModel):
    title:str
    description:str
    
    

class CreateMovie(BaseMovie):
    genres : list[int] 
    director : int 

class ResponseMovie(BaseMovie):
    id : int
    genres:list[BaseGenre]
    director :BaseDirector

    model_config = ConfigDict(from_attributes=True)

class UpdateMovie(BaseModel):
    title :str|None = None
    description:str |None =None
    genres : list[int] |None = None
    director : int |None = None