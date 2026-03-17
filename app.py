from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Sample data
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

# Home
@app.route('/')
def home():
    return redirect(url_for('list_students'))

# -------------------------------
# VIEW STUDENTS (TABLE UI)
# -------------------------------
@app.route('/students')
def list_students():
    html = """
    <html>
    <head>
        <title>Student Manager</title>
        <style>
            body {
                font-family: Arial;
                background: #f4f6f9;
                padding: 20px;
            }
            h2 {
                text-align: center;
            }
            table {
                width: 80%;
                margin: auto;
                border-collapse: collapse;
                background: white;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            th, td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
                text-align: center;
            }
            th {
                background: #007BFF;
                color: white;
            }
            tr:hover {
                background: #f1f1f1;
            }
            .btn {
                padding: 6px 12px;
                text-decoration: none;
                border-radius: 5px;
                color: white;
            }
            .edit { background: #28a745; }
            .delete { background: #dc3545; }
            .add {
                display: block;
                width: 200px;
                margin: 20px auto;
                text-align: center;
                background: #007BFF;
            }
        </style>
    </head>
    <body>

    <h2>Student List</h2>

    <a class="btn add" href="/add_student_form">+ Add Student</a>

    <table>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Grade</th>
            <th>Section</th>
            <th>Actions</th>
        </tr>

        {% for s in students %}
        <tr>
            <td>{{s.id}}</td>
            <td>{{s.name}}</td>
            <td>{{s.grade}}</td>
            <td>{{s.section}}</td>
            <td>
                <a class="btn edit" href="/edit_student/{{s.id}}">Edit</a>
                <a class="btn delete" href="/delete_student/{{s.id}}" onclick="return confirm('Delete this student?')">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>

    </body>
    </html>
    """
    return render_template_string(html, students=students)

# -------------------------------
# ADD STUDENT FORM
# -------------------------------
@app.route('/add_student_form')
def add_student_form():
    html = """
    <h2 style="text-align:center;">Add Student</h2>
    <form method="POST" action="/add_student" style="width:300px;margin:auto;">
        Name:<br><input type="text" name="name" required><br><br>
        Grade:<br><input type="number" name="grade" required><br><br>
        Section:<br><input type="text" name="section" required><br><br>
        <button type="submit">Add</button>
    </form>
    <br>
    <div style="text-align:center;">
        <a href="/students">Back</a>
    </div>
    """
    return render_template_string(html)

# -------------------------------
# ADD STUDENT
# -------------------------------
@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        name = request.form.get("name")
        grade = int(request.form.get("grade"))
        section = request.form.get("section")

        new_student = {
            "id": max([s["id"] for s in students]) + 1 if students else 1,
            "name": name,
            "grade": grade,
            "section": section
        }

        students.append(new_student)
    except:
        return "Error adding student"

    return redirect(url_for('list_students'))

# -------------------------------
# DELETE STUDENT
# -------------------------------
@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('list_students'))

# -------------------------------
# EDIT STUDENT
# -------------------------------
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)

    if not student:
        return "Student not found", 404

    if request.method == 'POST':
        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]
        return redirect(url_for('list_students'))

    html = """
    <h2 style="text-align:center;">Edit Student</h2>
    <form method="POST" style="width:300px;margin:auto;">
        Name:<br><input type="text" name="name" value="{{student.name}}" required><br><br>
        Grade:<br><input type="number" name="grade" value="{{student.grade}}" required><br><br>
        Section:<br><input type="text" name="section" value="{{student.section}}" required><br><br>
        <button type="submit">Update</button>
    </form>
    <br>
    <div style="text-align:center;">
        <a href="/students">Back</a>
    </div>
    """
    return render_template_string(html, student=student)

# -------------------------------
# API
# -------------------------------
@app.route('/api/students')
def api_students():
    return jsonify(students)

# -------------------------------
# RUN
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
