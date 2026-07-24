from flask import Flask, render_template, request, redirect, url_for
from database import create_database, save_student, get_all_students, delete_student as delete_student_db, update_student, get_student_by_id, check_student_login, mark_attendance

app = Flask(__name__)

# Create Database
create_database()

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Contact Page
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            return redirect(url_for("admin_dashboard"))

        else:
            return "Invalid Admin Login"

    return render_template("login.html")

@app.route("/admin-dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/student-login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        roll_number = request.form["roll_number"]
        password = request.form["password"]

        student= check_student_login(roll_number, password)
        print("LOGIN DATA:", student)
        if student:
            return redirect(url_for("student_dashboard",id=student[0]))

        else:
            return "Invalid Student Login"
    return render_template("student_login.html")        

@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        student_name = request.form["student_name"]
        roll_number = request.form["roll_number"]
        course = request.form["course"]
        password = request.form["password"]


        save_student(
            student_name,
            roll_number,
            course,
            password
        )

        return redirect(url_for("students"))


    return render_template("add_student.html")

@app.route("/students")
def students():

    students = get_all_students()

    return render_template(
        "students.html",
        students=students
    )
  
# Search Student
@app.route("/search")
def search():

    query = request.args.get("query")

    students = get_all_students()

    if query:
        students = [
            student for student in students
            if query.lower() in student[1].lower()
        ]

    return render_template(
        "students.html",
        students=students
    )

@app.route("/edit-student/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    student = get_student_by_id(id)

    if request.method == "POST":

        name = request.form["name"]
        roll_number = request.form["roll_number"]
        course = request.form["course"]

        update_student(
            id,
            name,
            roll_number,
            course
        )

        return redirect(url_for("students"))

    return render_template(
        "edit_student.html",
        student=student
    )

@app.route("/delete/<int:id>")
def delete(id):

    delete_student_db(id)

    return redirect(url_for("students"))

@app.route("/student-dashboard/<int:id>")
def student_dashboard(id):

    student = get_student_by_id(id)

    return render_template(
        "student_dashboard.html",
        student=student
    )

@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    students = get_all_students()

    if request.method == "POST":

        student_id = request.form["student_id"]
        status = request.form["status"]

        mark_attendance(student_id, status)

        return redirect(url_for("attendance"))

    return render_template(
        "attendance.html",
        students=students
    )
if __name__ == "__main__":
    app.run(debug=True)