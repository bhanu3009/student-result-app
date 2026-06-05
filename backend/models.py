from database import get_db_connection

def create_tables():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 1. Users Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role ENUM('admin', 'student') NOT NULL
                );
            """)
            
            # 2. Students Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    roll_no VARCHAR(50) UNIQUE NOT NULL,
                    class VARCHAR(50) NOT NULL
                );
            """)
            
            # 3. Subjects Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) UNIQUE NOT NULL
                );
            """)
            
            # 4. Results Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    subject_id INT NOT NULL,
                    marks INT NOT NULL,
                    grade VARCHAR(5) NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
                );
            """)
            
        connection.commit()
        print("Success: All tables created in student_db!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    create_tables()