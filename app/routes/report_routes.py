from fastapi import APIRouter,HTTPException

from database.book_db import book_table
from database.member_db import members_table

router = APIRouter()

@router.get("/summary")
def books_total_count():
    total =  book_table.books_total_count()
    return {f"total_books:{total}"}

@router.get("/summary")
def count_available_books():
    try:
        total = book_table.count_available_books()
        print(total)
        return {f"available_books:{total}"}
    except HTTPException:
            raise
    except Exception as e:
            raise HTTPException(status_code=500,detail=f"error{e}")
    

@router.get("/books-by-genre")
def count_by_genre():
    try:
        books_by_genere = book_table.count_by_genre()
        return books_by_genere
    except HTTPException:
            raise
    except Exception as e:
            raise HTTPException(status_code=500,detail=f"error{e}")
    
    

@router.get("/top-member")
def get_top_member():
    try:
        return members_table.get_top_member()
    except HTTPException:
            raise
    except Exception as e:
            raise HTTPException(status_code=500,detail=f"error{e}")
    