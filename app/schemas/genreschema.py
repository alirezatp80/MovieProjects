from pydantic import BaseModel 

class BaseGenre(BaseModel):
    name:str

class CreateGenre(BaseGenre):
    pass

class ResponseGenre(BaseGenre):
    id:int

class UpdateGenre(BaseGenre):
    name:str|None = None