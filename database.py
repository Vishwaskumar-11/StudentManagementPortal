import sqlite3

DATABASE = "students.db"

def create_database():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            roll_number TEXT UNIQUE NOT NULL,

            course TEXT NOT NULL,

            password TEXT NOT NULL

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_id INTEGER NOT NULL,

            attendance_date TEXT NOT NULL,

            status TEXT NOT NULL,

            FOREIGN KEY(student_id) REFERENCES students(id)

        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO admins(username, password)
        VALUES('admin', 'admin123')
    """)

    conn.commit()
    conn.close()

    print("Database Created Successfully!")

def save_student(name, roll_number, course, password):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (name, roll_number, course, password)

    VALUES(?,?,?,?)
    """,
    (
        name,
        roll_number,
        course,
        password
    ))

    conn.commit()
    conn.close()

    print("Student Saved Successfully!")

def get_all_students():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students"
    )

    students = cursor.fetchall()

    conn.close()

    return students

def update_student(id, name, roll_number, course):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE students

    SET name=?,
        roll_number=?,
        course=?

    WHERE id=?
    """,
    (
        name,
        roll_number,
        course,
        id
    ))

    conn.commit()
    conn.close()

    print("Student Updated Successfully!")

def delete_student(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM students
    WHERE id=?
    """,
    (id,))

    conn.commit()
    conn.close()

    print("Student Deleted Successfully!")

def search_student(keyword):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM students

    WHERE name LIKE ?
    OR roll_number LIKE ?

    """,
    (
        "%" + keyword + "%",
        "%" + keyword + "%"
    ))

    students = cursor.fetchall()

    conn.close()

    return students

def check_student_login(roll_number, password):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM students
    WHERE roll_number=?
    AND password=?

    """,
    (
        roll_number,
        password
    ))

    student = cursor.fetchone()

    conn.close()

    return student

def get_student_by_id(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()
    print(student)
    conn.close()

    return student    

from datetime import date

def mark_attendance(student_id, status):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    today = date.today().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO attendance (student_id, attendance_date, status)
        VALUES (?, ?, ?)
    """, (student_id, today, status))

    conn.commit()
    conn.close()

    print("Attendance Saved Successfully!")    