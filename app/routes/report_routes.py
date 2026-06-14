from fastapi import APIRouter,HTTPException
import logging
from database.book_db import book_table
from database.member_db import members_table

router = APIRouter()

logging.basicConfig(level= logging.INFO,format="%(asctime)s |%(level)s| %(message)s",filename="app/app.log")
logger =logging.getLogger(__name__)

@router.get("/summary")
def books_total_count():
    try:
        logger.info(f"GET/reports/summary called")
        total_books =  book_table.books_total_count()
        available_books = book_table.count_available_books()
        currently_borrowed = book_table.count_borrowed_books()
        active_members = members_table.count_active_members()
        return {f"""total books:{total_books},
                    available books":f"{available_books},
                    currently borrowed:{currently_borrowed},
                    active_members:{active_members}"""}

    except Exception as e:
            
            raise HTTPException(status_code=500,detail=f"error{e}")
    
@router.get("/books-by-genre")
def count_by_genre():
    try:
        logger.info(f"GET/reports/books-by-genre")
        books_by_genre = book_table.count_by_genre()
        books_by_genre = book_table.count_by_genre()
        return [f"{{{book['genre']}: {book['COUNT(*)']}}}" for book in books_by_genre]
    
   
    except Exception as e:
            raise HTTPException(status_code=500,detail=f"error{e}")
    
    

@router.get("/top-member")
def get_top_member():
    try:
        logger.info(f"GET/reports/top-member")
        top = members_table.get_top_member()
        if not top:
            logger.info("No found top")
            return {"message": "No members found"}
        logger.info(f"found top id:{top[0]}")
        return {"member_id": top[0],
                "borrows_total": top[1]}  
    except Exception as e:
            logger.error(f"Server error: {e}")
            raise HTTPException(status_code=500,detail=f"error{e}")
    