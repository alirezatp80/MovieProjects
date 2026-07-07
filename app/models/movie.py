
from sqlalchemy import Column , String , Integer  , ForeignKey , Table
from app.database import Base
from sqlalchemy.orm import relationship

movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id' , ForeignKey('movies.id') , primary_key=True),
    Column('genre_id' , ForeignKey('genres.id') , primary_key=True)
)


class Genre(Base):
    __tablename__ = 'genres'
    id =  Column(Integer , autoincrement=True , primary_key= True)
    name = Column(String(100) , nullable=False,unique=True)

    movies = relationship("Movie" , secondary=movie_genres,back_populates="genres")

class Director(Base):
    __tablename__ = 'directors'
    id = Column(Integer,autoincrement=True , primary_key=True)
    fullname = Column(String(150) , nullable=False , unique=True)

    movies= relationship('Movie' , back_populates="director")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer,primary_key=True , autoincrement=True)
    title = Column(String(250) , nullable= False , unique=True)
    description = Column(String)

    
    director_id = Column(Integer ,ForeignKey('directors.id'))
    director = relationship('Director' , back_populates='movies')

    genres = relationship('Genre' ,secondary=movie_genres, back_populates='movies')
   

