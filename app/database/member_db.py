from database import db_connection
import mysql.connector
from pydantic import BaseModel

class Member(BaseModel):
    name:str
    email:str
    total_borrows:int = 0

class Members:
    def __init__(self):
        pass

    def create_member(self,data):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql_insert = """INSERT INTO members (name,email) 
        VALUES (%s,%s);"""
        values = (data["name"], data["email"])
        try:
            cursor.execute(sql_insert,values)
            conn.commit()
            rows = cursor.lastrowid
            return rows
        except Exception as e:
             return e
        finally:
            cursor.close()
            conn.close()

    def get_all_members(self):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql_all_members = "SELECT * FROM members;"
        try:       
            cursor.execute(sql_all_members)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            return e
     
        finally:
            cursor.close()
            conn.close() 

    def get_member_by_id(self,id):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql_member_by_id = "SELECT * FROM members WHERE id = %s"
        try:
            cursor.execute(sql_member_by_id,(id,))     
            row = cursor.fetchone()
            return row
        except Exception as e:
            return e   
        finally:
            cursor.close()
            conn.close()
        
    def update_member(self,id:int,data:dict)-> bool:
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        set_cluse = ", ".join([f"{key} = %s" for key in data.keys()])
        sql_update = f"UPDATE members SET {set_cluse} WHERE ID = %s;"
        values = list(data.values()) + [id]
        try:
        
            cursor.execute(sql_update,(values))
            conn.commit()
            rows = cursor.rowcount
            return rows > 0

        except Exception as e:
            raise e   
        finally:
            cursor.close()
            conn.close()

    def deactivate_member(self,id):
         
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql_update_book = """UPDATE members
                             SET is_active=False WHERE id = %s""" 
        values = (id) 

        try:
            cursor.execute(sql_update_book,(values))
            conn.commit()
            cursor.close()
            rows = cursor.rowcount
            return rows > 0
        except Exception as e:
            raise e   
        finally:
            cursor.close()
            conn.close()
    def activate_member(self,id):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql_update_book = """UPDATE members
                             SET is_active=TRUE WHERE id = %s""" 
        values = (id) 

        try:
            cursor.execute(sql_update_book,(values))
            conn.commit()
            cursor.close()
            rows = cursor.rowcount
            return rows > 0
        except Exception as e:
            raise e   
        finally:
            cursor.close()
            conn.close()

    def increment_borrows(self,id):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql_increment_borrows = """UPDATE members
                             SET borrows_total + 1 WHERE id = %s""" 
        values = (id)
        try:
            cursor.execute(sql_increment_borrows,(values))
            conn.commit()
            rows = cursor.rowcount
            return rows > 0
        except Exception as e:
            raise e   
        finally:
            cursor.close()
            conn.close() 