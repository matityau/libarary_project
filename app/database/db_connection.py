import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
    host = "localhost",
    port ="3306"
    user = "root",
    password ="root",
    database = "libarary_db"
    use_pure=True
    )                    
    return conn

def create_book_table():
    sql = """
        CREATE TABLE books IF NOT EXSIST() """