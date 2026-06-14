from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from database import member_db
from database.member_db import members_table
from pydantic import BaseModel
from typing import Optional
import logging

router = APIRouter()


logging.basicConfig(level= logging.INFO,format="%(asctime)s |%(level)s| %(message)s",filename="app/app.log")
logger =logging.getLogger(__name__)

class Member(BaseModel):
    name:str
    email:str

@router.get("")
def get_all_members():
    return members_table.get_all_members()

@router.post("")
def create_member(data:Member):
    try:
        logger.info("POST/member called")
        book_dict = data.model_dump()
        new_member = members_table.create_member(book_dict)
        logger.info(f"create a {new_member} member")
        return{"message":"Member created successfully","Member_id":new_member}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Server Error:{e}")
        raise HTTPException(status_code=500,detail=f"{e}")
    


@router.get("/{id}")
def get_member_by_id(id:int):
    try:
        logger.info(f"GET/books/{id} called")
        found = members_table.get_member_by_id(id)
        if found:
            logger.info(f"meber id:{id} found")
            return found
        logger.error(f"member id:{id} not found")
        raise HTTPException(status_code=404,detail=f"book {id} not found ")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Server Error:{e}")
        raise HTTPException(status_code=500,detail=f"error{e}")
    
@router.patch("/{id}")
def update_member(id,data:Member):
    logger.info(f"PATCH/members/{id}")
    dict_data = data.model_dump(exclude_none=True)

    if not dict_data:
        logger.warning("Not data filled")
        raise HTTPException(status_code=400, detail="No filed data")
    
    update = members_table.update_member(id,dict_data)

    if not update:
        logger.warning(f"member id:{id} not found")
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message":f"book {id}","filed_update":dict_data}


@router.patch("/{id}/deactive")
def deactivate_member(id:int):
    logger.info(f"PATCH/member/{id}")

    update = members_table.deactivate_member(id)

    if not update:
        logger.warning(f"Member {id} not found")
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message":f"Mmeber {id} now is deactive"}
 

# @router.patch("/{id}/activate")