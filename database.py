import mysql.connector

my_db = mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    password= 'thaalibiya',
    database= 'testdb'
)

my_cursor = my_db.cursor()

def tables():
    queue= "SHOW TABLES"
    my_cursor.execute(queue)
    for i in my_cursor :
        print(f"current tables are : {i}")
    
def create_table():
    queue = """CREATE TABLE user (
        email VARCHAR(15) PRIMARY KEY,
        username VARCHAR(10) NOT NULL,
        password VARCHAR(10) NOT NULL)"""
    
    my_cursor(queue)
    print("table created !")

tables()