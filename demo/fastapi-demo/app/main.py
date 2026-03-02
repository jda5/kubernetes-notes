from contextlib import asynccontextmanager

import mysql.connector
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from starlette.config import Config

# -------------------------------------------------------------------------------- models


class BookTitle(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)


class Book(BookTitle):
    id: int


# -------------------------------------------------------------------------------- queries

CREATE_DATABASE = """
CREATE DATABASE IF NOT EXISTS books_db;

CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL
);

USE books_db;
"""

INSERT_BOOK = """
INSERT INTO books (title)
VALUES (%s)
"""

SELECT_BOOK = """
SELECT 
    id, title 
FROM 
    books 
WHERE 
    id = %s
"""

SELECT_BOOKS = """
SELECT 
    id, title 
FROM 
    books
"""

# -------------------------------------------------------------------------------- setup

config = Config(".env")

MYSQL_USER = config("MYSQL_USER")
MYSQL_PASSWORD = config("MYSQL_PASSWORD")

connection = None
cursor = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    global connection, cursor # pylint: disable=global-statement
    connection = mysql.connector.connect(
        host="db",
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=3306,
        autocommit=True,
    )
    cursor = connection.cursor()
    cursor.execute(CREATE_DATABASE)
    yield
    cursor.close()
    connection.close()


app = FastAPI(lifespan=lifespan)

# -------------------------------------------------------------------------------- routes


@app.get("/books/{book_id}")
def get_book(book_id: int) -> Book:
    cursor.execute(SELECT_BOOK, (book_id,))
    result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(id=result[0], title=result[1])


@app.get("/books")
def get_books() -> list[Book]:
    cursor.execute(SELECT_BOOKS)
    results = cursor.fetchall()
    return [Book(id=row[0], title=row[1]) for row in results]


@app.post("/books")
def post_book(title: BookTitle) -> Book:
    cursor.execute(INSERT_BOOK, (title.title,))
    book_id = cursor.lastrowid
    return Book(id=book_id, title=title.title)
