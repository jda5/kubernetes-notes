from contextlib import asynccontextmanager
from typing import Annotated

import mysql.connector
from mysql.connector.abstracts import MySQLCursorAbstract
from fastapi import FastAPI, HTTPException, Depends
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
"""

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS books_db.books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL
);
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

MYSQL_ROOT_PASSWORD = config("MYSQL_ROOT_PASSWORD")

def get_cursor():
    """
    Helper to create a fresh cursor
    """
    conn = mysql.connector.connect(
        host="db",
        user="root",
        database="books_db",
        password=MYSQL_ROOT_PASSWORD,
        port=3306,
        autocommit=True,
    )
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        cursor.close()
        conn.close()

@asynccontextmanager
async def lifespan(_: FastAPI):
    conn = mysql.connector.connect(
        host="db",
        user="root",
        password=MYSQL_ROOT_PASSWORD,
        port=3306,
        autocommit=True,
    )
    cursor = conn.cursor()
    cursor.execute(CREATE_DATABASE)
    cursor.execute(CREATE_TABLE)
    cursor.close()
    conn.close()
    yield


app = FastAPI(lifespan=lifespan)

# -------------------------------------------------------------------------------- routes


@app.get("/books/{book_id}")
def get_book(book_id: int, cursor: Annotated[MySQLCursorAbstract, Depends(get_cursor)]) -> Book:
    cursor.execute(SELECT_BOOK, (book_id,))
    result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(id=result[0], title=result[1])


@app.get("/books")
def get_books(cursor: Annotated[MySQLCursorAbstract, Depends(get_cursor)]) -> list[Book]:
    cursor.execute(SELECT_BOOKS)
    results = cursor.fetchall()
    return [Book(id=row[0], title=row[1]) for row in results]


@app.post("/books")
def post_book(title: BookTitle, cursor: Annotated[MySQLCursorAbstract, Depends(get_cursor)]) -> Book:
    cursor.execute(INSERT_BOOK, (title.title,))
    book_id = cursor.lastrowid
    return Book(id=book_id, title=title.title)
