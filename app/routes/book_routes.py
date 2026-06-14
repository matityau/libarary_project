from fastapi import APIRouter,HTTPException
from database import book_db
from database.book_db import book_table
from database.member_db import members_table
from pydantic import BaseModel
from typing import Optional
import logging 


logging.basicConfig(level=logging.INFO,format="%(asctime)s|%(levelname)s|%(message)s",filename="logs/app.log")
logger = logging.getLogger(__name__)

router = APIRouter()



class Book(BaseModel):
    title:str
    author:str
    genre:str 

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None

@router.get("")
def view_all_books():
    try:
        logger.info("GET /books called")
        return book_table.get_all_books()
    except Exception as e:
        logger.error(f"Server error:{e}")
        raise HTTPException(status_code=500,detail="server crashed")

@router.post("")
def create_book(data:Book):
    geners = ["Fiction","Non-Fiction","Science","History","Other"]
    try:
        logger.info("POST/books called")
        book_dict = data.model_dump()
        if not data.genre in geners:
            logger.warning(f"Data {data.genre} not correctly")
            raise HTTPException(status_code=400,detail="the optiotionl geners is:Fiction,Non-Fiction, Science,History,Other")
        new_book = book_table.create_book(book_dict)
        logger.info(f"create a {new_book} book")
        return{"message":"Book created successfully","book_id":new_book}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Server Error:{e}")
        raise HTTPException(status_code=500,detail=f"{e}")
    
@router.get("/{id}")
def get_book_by_id(id:int):
    try:
        logger.info(f"GET/books/{id} called")
        found = book_table.get_book_by_id(id)
        if found:
            logger.info(f"Book {id} found")
            return found
        logger.error(f"Book {id} not found")
        raise HTTPException(status_code=404,detail=f"book {id} not found ")
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Server Error")
        raise HTTPException(status_code=500,detail=f"error{e}")
    
@router.patch("/{id}")
def update_book(id,data:BookUpdate):
    try:    
        logger.info(f"PATCH/books/{id}")
        dict_data = data.model_dump(exclude_none=True)

        if not dict_data:
            logger.warning("Not data filled")
            raise HTTPException(status_code=400, detail="No filed data")
        
        update = book_table.update_book(id,dict_data)

        if not update:
            logger.warning(f"Book {id} not found")
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message":f"book {id}","filed_update":dict_data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Server Error:{e}")
        raise HTTPException(status_code=500,detail=f"error{e}")
    

@router.patch("/{id}/borrow/{member_id}")
def borrow_book(book_id:int,member_id:int):
    try:
        logger.info(f"PUT/books {id} borrow/{member_id}")
        book = book_table.get_book_by_id(book_id)
        if not book:
            logger.error(f"Book {book_id} not found")
            raise HTTPException(status_code=404,detail=f"Book id:{book_id}not found")
        member = members_table.get_member_by_id(member_id)
        
        if not member:
            logger.error(f"member {member_id} not found")
            raise HTTPException(status_code=404,detail="Member not found")
        sucsses = book_table.set_available(book_id,False,member_id)
        print(sucsses)
        if not sucsses: 
            logger.info(f"book not update")   
            raise HTTPException(status_code=400,detail=f"Book id:{book_id} is not available")
        members_table.increment_borrows(member_id)
        logger.info(f"book{id} borrow by {member_id}") 
        return {"messaage":f"The book {book_id} is borrow by  member{member_id}"}
   
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Server Error:{e}")
        raise HTTPException(status_code=500,detail=f"error{e}")
    


    


            
    