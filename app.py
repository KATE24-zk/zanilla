from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Sample data
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

# Home redirect
@app.route('/')
def home():
    return redirect(url_for('list_students'))

# -------------------------------
# VIEW STUDENTS
# -------------------------------
@app.route('/students')
def list_students():
    html = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Student Manager</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: #f0f2f5; }
            .table-container { margin-top: 50px; }
            .btn-add { margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
          <div class="container">
            <a class="navbar-brand" href="/students">Student Manager</a>
          </div>
        </nav>

        <div class="container table-container">
            <div class="text-center">
                <a href="/add_student_form" class="btn btn-success btn-add">+ Add Student</a>
            </div>
            <div class="card shadow-sm">
                <div class="card-body">
                    <table class="table table-hover text-center">
                        <thead class="table-primary">
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Grade</th>
                                <th>Section</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                        {% for s in students %}
                            <tr>
                                <td>{{ s.id }}</td>
                                <td>{{ s.name }}</td>
                                <td>{{ s.grade }}</td>
                                <td>{{ s.section }}</td>
                                <td>
                                    <a class="btn btn-sm btn-warning" href="/edit_student/{{s.id}}">Edit</a>
                                    <a class="btn btn-sm btn-danger" href="/delete_student/{{s.id}}" onclick="return confirm('Delete this student?')">Delete</a>
                                </td>
                            </tr>
                        {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
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
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Add Student</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body style="background:#f0f2f5;">
        <div class="container mt-5">
            <div class="card shadow-sm mx-auto" style="max-width: 400px;">
                <div class="card-body">
                    <h3 class="card-title text-center mb-4">Add Student</h3>
                    <form method="POST" action="/add_student">
                        <div class="mb-3">
                            <label class="form-label">Name</label>
                            <input type="text" name="name" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Grade</label>
                            <input type="number" name="grade" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Section</label>
                            <input type="text" name="section" class="form-control" required>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">Add Student</button>
                        </div>
                    </form>
                    <div class="text-center mt-3">
                        <a href="/students">Back to List</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

# -------------------------------
# EDIT STUDENT FORM
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
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Edit Student</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body style="background:#f0f2f5;">
        <div class="container mt-5">
            <div class="card shadow-sm mx-auto" style="max-width: 400px;">
                <div class="card-body">
                    <h3 class="card-title text-center mb-4">Edit Student</h3>
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Name</label>
                            <input type="text" name="name" class="form-control" value="{{student.name}}" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Grade</label>
                            <input type="number" name="grade" class="form-control" value="{{student.grade}}" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Section</label>
                            <input type="text" name="section" class="form-control" value="{{student.section}}" required>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-warning">Update Student</button>
                        </div>
                    </form>
                    <div class="text-center mt-3">
                        <a href="/students">Back to List</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, student=student)

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
