from fastapi import APIRouter,HTTPException
from database import book_db
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
book_table = book_db.Books()

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
        return book_table.get_all_books()
    except Exception as e:
        raise HTTPException(status_code=500,detail="server crashed")

@router.post("")
def create_book(data:Book):
    geners = ["Fiction","Non-Fiction","Science","History","Other"]
    try:
        book_dict = data.model_dump()
        if not data.genre in geners:
            raise HTTPException(status_code=400,detail="the optiotionl geners is:Fiction,Non-Fiction, Science,History,Other")
        new_book = book_table.create_book(book_dict)
        return{"message":"Book created successfully","book_id":new_book}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    
@router.get("/{id}")
def get_book_by_id(id:int):
    try:
        found = book_table.get_book_by_id(id)
        if found:
            return found
        raise HTTPException(status_code=404,detail=f"book {id} not found ")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error{e}")
    
@router.patch("/{id}")
def update_book(id,data:BookUpdate):

    dict_data = data.model_dump(exclude_none=True)

    if not dict_data:
        raise HTTPException(status_code=400, detail="No filed data")
    
    update = book_table.update_book(id,dict_data)

    if not update:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message":f"book {id}","filed_update":dict_data}

@router.put("/{id}/borrow/{member_id}")
def borrow_book(book_id:int,member_id:int):
    
    book = book_table.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404,detail="Member not found")
    sucsses = book_table.set_available(book_id,False,member_id)
    if not sucsses:    
        raise HTTPException(status_code=400,detail=f"Book is not available")
    return {"messaage":f"The book {book_id} is borrow by  member{member_id}"}


    


            
    