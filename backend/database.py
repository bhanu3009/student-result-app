import os
import pymysql
from dotenv import load_dotenv
load_dotenv() 

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = os.getenv("DB_PASSWORD", "")  
DB_NAME = "student_db"

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )