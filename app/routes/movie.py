from fastapi import APIRouter , Depends , status , HTTPException , Query
from sqlalchemy.orm import Session 
from app.models.movie import Movie , Genre , Director
from app.schemas.movieschema import ResponseMovie  ,UpdateMovie,CreateMovie
from app.schemas.genreschema import BaseGenre
from app.database import get_db
app = APIRouter(prefix='/movie' , tags=['Movie'])

@app.get('/search' , response_model=list[ResponseMovie])
def get_by_title(query:str = Query(... , min_length=1 ) , db:Session=Depends(get_db)):
   movies = (
        db.query(Movie)
        .filter(Movie.title.ilike(f"%{query}%"))
        .all()
    )
   return movies

@app.get('/filter_by_genre',response_model=list[ResponseMovie])
def get_by_genre(genre_inp:str , db:Session=Depends(get_db)):
   genre = db.query(Genre).filter(Genre.name == genre_inp).first()
   if genre is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail='not found genre'
      )
   return genre.movies

@app.get('/filter_by_director',response_model=list[ResponseMovie])
def get_by_director(director:str , db:Session=Depends(get_db)):
   director_db = db.query(Director).filter(Director.fullname == director).first()
   if director_db is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail='not found Director'
      )
   return director_db.movies


@app.post('/' , response_model=ResponseMovie , status_code=status.HTTP_201_CREATED)
def create_movie(movie: CreateMovie , db:Session=Depends(get_db)):
   if db.query(Movie).filter(Movie.title == movie.title).first():
      raise HTTPException(
         status_code=status.HTTP_409_CONFLICT,
         detail='Movie already exist!!!'
      )
   director = (
      db.query(Director)
      .filter(Director.id == movie.director)
      .first()
   )
   if director is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail="Cant find Director !!!"
      )
   genres = (
      db.query(Genre)
      .filter(Genre.id.in_(movie.genres))
      .all()
   )
   if len(genres) != len(movie.genres):
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail='cant find one or more genres'
      )
   newmovie = Movie(
      title = movie.title,
      description = movie.description,
      genres = genres,
      director = director,
   )
   try:
      db.add(newmovie)
      db.commit()
      db.refresh(newmovie)
   except:
      raise HTTPException(
         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
         detail='Database Has Error!!!'
      )
   return newmovie

@app.get('/' , response_model=list[ResponseMovie] )
def get_all_movie(db:Session=Depends(get_db)):
   try:
    movies = db.query(Movie).all()
   except:
      raise HTTPException(
         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
         detail='database has error!!!'
      )
   return movies

@app.get('/{movie_id}' , response_model=ResponseMovie)
def get_movie(movie_id:int , db:Session=Depends(get_db)):
   db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
   if db_movie is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail='Cant find movie'
      )
   return db_movie

@app.patch('/{movie_id}' , response_model=ResponseMovie)
def update_movie(movie_id:int , movie:UpdateMovie , db:Session=Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if (db_movie) is None:
       raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail='cant find Movie'
       )
    if (db.query(Movie).filter(Movie.title == movie.title).first()):
       raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail='Title is duplicated !!! '
       )
     
    update_movie = movie.model_dump(exclude_unset=True)
    for key, value in update_movie.items():
        if key not in ["director", "genres"]:
            setattr(db_movie, key, value)

    # بروزرسانی کارگردان
        if "director" in update_movie:
            director = db.query(Director).filter(
                Director.id == update_movie["director"]
            ).first()

            if director is None:
                raise HTTPException(
                    status_code=404,
                    detail="Director not found"
                )

            db_movie.director = director

        # بروزرسانی ژانرها
        if "genres" in update_movie:
            genres = db.query(Genre).filter(
                Genre.id.in_(update_movie["genres"])
            ).all()

            if len(genres) != len(update_movie["genres"]):
                raise HTTPException(
                    status_code=404,
                    detail="One or more genres not found"
                )

            db_movie.genres = genres

    try:
        db.commit()
        db.refresh(db_movie)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

    return db_movie
   
@app.delete('/{movie_id}' , status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id ,  db:Session=Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if (db_movie) is None:
       raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail='cant find Movie'
       )
    try:
       db.delete(db_movie)
       db.commit()
    except:
       db.rollback()
       raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail='Database has Error!!!'
       )

