from fastapi import FastAPI,HTTPException
from pymongo import MongoClient
from models import Book
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI= os.environ.get("MONGODB_URI")

app = FastAPI()

client = MongoClient(MONGODB_URI)
db = client["my_book_database"]
collection = db["books"]


@app.post("/books", response_model=Book)
async def create_book(book: Book):
  book_dict = book.dict()
  collection.insert_one(book_dict)
  return book

@app.get("/books")
async def get_books():
  books = []
  for book in collection.find():
    books.append(Book(**book))
  return books


@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
  book = collection.find_one({"_id": ObjectId(book_id)})
  if book:
    return Book(**book)
  else:
    raise HTTPException(status_code=404, detail="Book not found")
  

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: str, book: Book):
  book_dict = book.dict()
  collection.update_one({"_id": ObjectId(book_id)}, {"$set": book_dict})
  return book


@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
  collection.delete_one({"_id": ObjectId(book_id)})
  return {"message": "Book deleted successfully"}
