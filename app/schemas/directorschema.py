from pydantic import BaseModel



class BaseDirector(BaseModel):
    fullname:str

class CreateDorector(BaseDirector):
    pass 

class ResponseDirector(BaseDirector):
    id :int