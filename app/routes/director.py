from fastapi import APIRouter , status , HTTPException ,Depends
from sqlalchemy.orm import Session
from app.schemas.directorschema import CreateDorector , ResponseDirector
from app.models.movie import Director
from app.database import get_db

app = APIRouter(prefix='/director' , tags=['Director'])

@app.post('/',response_model=ResponseDirector)
def create_director(director:CreateDorector , db:Session=Depends(get_db)):
    db_director = db.query(Director).filter(Director.fullname == director.fullname).one_or_none()
    if db_director is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail='director duplicate')
    newdirector = Director(fullname=director.fullname)
    try:
        db.add(newdirector)
        db.commit()
        db.refresh(newdirector)
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail='database error')
    return newdirector