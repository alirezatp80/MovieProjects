from fastapi import APIRouter , Depends , HTTPException , status
from app.schemas.movieschemas import CreateGenre , ResponseGenre
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
    
    
