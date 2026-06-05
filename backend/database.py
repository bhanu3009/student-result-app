import pymysql
import os
from dotenv import load_dotenv

# This loads the local .env file when you test on your laptop
load_dotenv()

def get_db_connection():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),  # <--- NEW: Tells Python to listen to custom ports
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "your_local_password"),
        database=os.getenv("DB_NAME", "student_db"),
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection