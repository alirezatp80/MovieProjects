import http
import stat

from fastapi import APIRouter , status , HTTPException ,Depends
from sqlalchemy.orm import Session
from app.schemas.directorschema import CreateDorector , ResponseDirector,UpdateDirector
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

@app.get('/' , response_model=list[ResponseDirector])
def get_all_directors(db:Session=Depends(get_db)):
    try:
        directors = db.query(Director).all()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail='db has error!!')
    return directors

@app.get('/{director_id}' , response_model=ResponseDirector)
def get_director(director_id:int , db:Session=Depends(get_db)):
    db_director = db.query(Director).filter(Director.id == director_id).one_or_none()
    if db_director is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='cant find directors')
    return db_director

@app.patch('/{director_id}' , response_model=ResponseDirector)
def edit_director(director_id :int , director : UpdateDirector , db:Session=Depends(get_db)):
    db_director = db.query(Director).filter(Director.id == director_id).one_or_none()
    if db_director is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='cant find director')
    check_director = db.query(Director).filter(Director.fullname == director.fullname).one_or_none()
    if check_director is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail='name is duplicate!!')
    update_director = director.model_dump(exclude_unset=True)
    for key , value in update_director.items():
        setattr(db_director,key,value)
    try:
        db.commit()
        db.refresh(db_director)
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail='databse has error !!!!')
    return db_director

@app.delete('/{director_id}' , status_code=status.HTTP_204_NO_CONTENT)
def delete_director(director_id :int , db:Session=Depends(get_db)):
    db_director = db.query(Director).filter(Director.id == director_id).one_or_none()
    if db_director is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='not find director')
    try:
        db.delete(db_director)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail='database has error')


