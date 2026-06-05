import pymysql

# A list of the most likely passwords based on your history and common defaults
passwords_to_try = [
    "Surya150150",   # Without the hash (URL parsing theory)
    "Surya150150#",  # With the hash
    "",              # Blank
    "1234#",
    "root",          # Common default
    "admin",         # Common default
    "1234",          # Common default
    "12345678"       # Common default
]

print("Starting local brute-force test...")

winning_password = None

for pwd in passwords_to_try:
    try:
        # Attempt connection
        conn = pymysql.connect(host="localhost", user="root", password=pwd)
        winning_password = pwd
        
        # If we get here, the password worked! Let's create the database.
        conn.cursor().execute("CREATE DATABASE IF NOT EXISTS student_db;")
        conn.close()
        break # Stop guessing
        
    except pymysql.err.OperationalError:
        print(f"[FAILED] Password rejected: '{pwd}'")

if winning_password is not None:
    print(f"\n[SUCCESS] 🔓 ACCESS GRANTED! Your correct password is: '{winning_password}'")
    print("Database 'student_db' has been successfully created!")
else:
    print("\n[LOCKED OUT] None of the passwords worked. We will need to bypass the database completely.")



# Email: admin@test.com

# Password: mysecretpassword