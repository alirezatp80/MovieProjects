from fastapi import APIRouter , Depends , HTTPException , status
from app.schemas.genreschema import CreateGenre , ResponseGenre , UpdateGenre
from app.database import get_db
from sqlalchemy.orm import Session 
from app.models.movie import Genre

app = APIRouter(prefix='/genre' , tags=['Genre'])

@app.post('/' , response_model=ResponseGenre )
def createGenre(genre : CreateGenre ,db:Session=Depends(get_db)): # type: ignore
        chack_genre = db.query(Genre).filter(Genre.name == genre.name).one_or_none() # type: ignore
        if chack_genre :
              raise  HTTPException(status_code=status.HTTP_409_CONFLICT ,detail='genre is duplicate')
        newgenre = Genre(name=genre.name)
        try:
            db.add(newgenre)
            db.commit()
            db.refresh(newgenre)
        except:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail='database exception!!!')
        return newgenre
    
@app.get('/',response_model=list[ResponseGenre])
def get_all_genre(db:Session=Depends(get_db)):
    try:
        genres = db.query(Genre).all()
        return genres
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail='cant fetch data from database !!! ')

@app.get('/{genre_id}',response_model=ResponseGenre)
def get_genre(genre_id:int,db:Session=Depends(get_db)):
     genre = db.query(Genre).filter(Genre.id == genre_id).one_or_none()
     if genre is None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='cant find genre')
     return genre

@app.patch('/{genre_id}' , response_model=ResponseGenre)
def edit_genre(genre_id :int , genre:UpdateGenre , db:Session=Depends(get_db)):
     db_genre = db.query(Genre).filter(Genre.id == genre_id).one_or_none()
     if db_genre is None:
          raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail='cant find genre')
     update_genre = genre.model_dump(exclude_unset=True)
     for key , value in update_genre.items():
          setattr(db_genre,key,value)
     try:     
        db.commit()
        db.refresh(db_genre)
     except:
          db.rollback()
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail='database has error')
     return db_genre

@app.delete('/{genre_id}' , status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(genre_id:int ,db:Session=Depends(get_db)):
     db_genre= db.query(Genre).filter(Genre.id == genre_id).one_or_none()
     if db_genre is None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail='cant find genre')
     try:
          db.delete(db_genre)
          db.commit()
     except:
          db.rollback()
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail='database has error')
