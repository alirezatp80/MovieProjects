# 🎬 Movie API

A RESTful API built with **FastAPI** and **SQLAlchemy** for managing movies, genres, and directors.

## Features

* CRUD operations for Movies
* CRUD operations for Genres
* CRUD operations for Directors
* Search movies by title
* Filter movies by genre
* Filter movies by director
* SQLAlchemy ORM
* Pydantic validation
* Automatic API documentation with Swagger UI

---

## Tech Stack

* Python 3.x
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd MovieProject
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the project

```bash
python main.py
```

The API will be available at:

```
http://127.0.0.1:8080
```

---

## API Documentation

Swagger UI

```
http://127.0.0.1:8080/docs
```

ReDoc

```
http://127.0.0.1:8080/redoc
```

---

# API Endpoints

## Genre

| Method | Endpoint            | Description       |
| ------ | ------------------- | ----------------- |
| GET    | `/genre/`           | Get all genres    |
| POST   | `/genre/`           | Create a genre    |
| GET    | `/genre/{genre_id}` | Get a genre by ID |
| PATCH  | `/genre/{genre_id}` | Update a genre    |
| DELETE | `/genre/{genre_id}` | Delete a genre    |

---

## Director

| Method | Endpoint                  | Description          |
| ------ | ------------------------- | -------------------- |
| GET    | `/director/`              | Get all directors    |
| POST   | `/director/`              | Create a director    |
| GET    | `/director/{director_id}` | Get a director by ID |
| PATCH  | `/director/{director_id}` | Update a director    |
| DELETE | `/director/{director_id}` | Delete a director    |

---

## Movie

| Method | Endpoint                                        | Description               |
| ------ | ----------------------------------------------- | ------------------------- |
| GET    | `/movie/`                                       | Get all movies            |
| POST   | `/movie/`                                       | Create a movie            |
| GET    | `/movie/{movie_id}`                             | Get a movie by ID         |
| PATCH  | `/movie/{movie_id}`                             | Update a movie            |
| DELETE | `/movie/{movie_id}`                             | Delete a movie            |
| GET    | `/movie/search?title={title}`                   | Search movies by title    |
| GET    | `/movie/filter_by_genre?genre={genre}`          | Filter movies by genre    |
| GET    | `/movie/filter_by_director?director={director}` | Filter movies by director |

---

## Example Request

### Create Movie

```http
POST /movie/
```

```json
{
  "title": "Inception",
  "description": "A science fiction action film.",
  "genres": [1, 2],
  "director": 1
}
```

---

## Example Response

```json
{
  "id": 1,
  "title": "Inception",
  "description": "A science fiction action film.",
  "genres": [
    {
      "id": 1,
      "name": "Sci-Fi"
    },
    {
      "id": 2,
      "name": "Action"
    }
  ],
  "director": {
    "id": 1,
    "fullname": "Christopher Nolan"
  }
}
```

---

## Project Structure

```
MovieProject
│
├── app
│   ├── database.py
│   ├── models
│   ├── routes
│   ├── schemas
│   └── ...
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Author

Alirezatd80
