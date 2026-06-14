import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host = "localhost",
        port ="3306",
        user = "root",
        password ="root",
        database = "libarary",
        use_pure=True
        )                    
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    sql_table_books = """
            CREATE TABLE IF NOT EXISTS books(
            id INT PRIMARY  KEY AUTO_INCREMENT,
            title VARCHAR(50) NOT NULL,
            author VARCHAR(50) NOT NULL,
            genre ENUM("Fiction","Non-Fiction","Science","History","Other") NOT NULL,
            available_is BOOLEAN DEFAULT True,
            id_member_by_borrowed INT DEFAULT NULL
            ); """
    sql_table_members = """
            CREATE TABLE IF NOT EXISTS members(
            id INT PRIMARY  KEY AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            is_active BOOLEAN DEFAULT TRUE,
            borrows_total INT DEFAULT 0
            );"""
    
    cursor.execute(sql_table_books)
    cursor.execute(sql_table_members)
    conn.commit()
    cursor.close()
    conn.close()



