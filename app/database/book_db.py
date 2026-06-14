from database import db_connection
import mysql.connector


class Books:

    def __init__(self) -> None:
        self.conn = db_connection.get_connection()
        
    
    def create_book(self,data:dict):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql_insert = """INSERT INTO books (title,author,genre,is_available,borrowed_by=NULL) 
        VALUES (%s,%s,%s,%s);"""
        values = (data["title"], data["author"], data["genre"],True)
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
        
    
    def get_all_books(self):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql_all_books = "SELECT * FROM books;"
        try:       
            cursor.execute(sql_all_books)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            return e
     
        finally:
            cursor.close()
            conn.close()   



    def get_book_by_id(self,book_id:int):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql_book_by_id = "SELECT * FROM books WHERE id = %s"
        try:
            cursor.execute(sql_book_by_id,(book_id,))     
            row = cursor.fetchone()
            return row
        except Exception as e:
            return e   
        finally:
            cursor.close()
            conn.close()
        
    
    def update_book(self,book_id:int,data)->bool:
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        set_cluse = ", ".join([f"{key} = %s" for key in data.keys()])
        sql_update = f"UPDATE books SET {set_cluse} WHERE ID = %s;"
        values = list(data.values()) + [book_id]
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

    def set_available(self,book_id:int, val:bool,member_id:int)->bool:     
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql_update_book = """UPDATE books
                    SET is_available = %s,
                    borrowed_by_member_id=%s
                    WHERE id = %s;""" 
        values = (val,member_id,book_id) 

        try:
            if not val:
                cursor.execute("UPDATE books SET borrowed_by_member_id = 0 WHERE id = %s;",(book_id,))
            cursor.execute(sql_update_book,(values))
            conn.commit()
            
            rows = cursor.rowcount
            return rows > 0
        except Exception as e:
            raise e   
        finally:
            cursor.close()
            conn.close()


    def books_total_count(self):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql_count = "SELECT COUNT(*)as total  FROM books;"
        try:
            cursor.execute(sql_count)
            rows = cursor.fetchone()
            return rows["total"]
        
        except Exception as e:
            raise e   
        finally:
            cursor.close()
            conn.close()
    
    def count_available_books(self):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql_count = "SELECT COUNT(*) FROM books WHERE is_available = True;"
        try:
            cursor.execute(sql_count)
            rows = cursor.fetchall()
            return len(rows)
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def count_borrowed_books(self):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql_count = "SELECT COUNT(*) FROM books WHERE is_available = False;"
        try:
            cursor.execute(sql_count)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def count_by_genre(self):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql_count = "SELECT COUNT(*)as total FROM books order by genre;"
        try:
            cursor.execute(sql_count)
            rows = cursor.fetchone()
            return rows
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def count_active_borrows_by_member(self, member_id)->int:
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql_count = """SELECT COUNT(*) as total FROM books 
                   WHERE borrowed_by_member_id = %s AND is_available = FALSE;"""
        try:
            cursor.execute(sql_count,(member_id,))
            row = cursor.fetchone()
            return row["total"] if row else 0
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()


book_table = Books()