from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Sample data
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

# Shared Header/CSS Template
BASE_HEAD = """
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>EduFlow | Student Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { background-color: #f8f9fa; font-family: 'Inter', sans-serif; color: #334155; }
        .navbar { background: #ffffff !important; border-bottom: 1px solid #e2e8f0; }
        .navbar-brand { font-weight: 700; color: #2563eb !important; letter-spacing: -0.5px; }
        .card { border: none; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .stats-card { background: #fff; border-left: 4px solid #2563eb; }
        .table thead { background-color: #f1f5f9; }
        .btn-primary { background-color: #2563eb; border: none; padding: 10px 20px; font-weight: 600; border-radius: 8px; }
        .btn-warning { background-color: #f59e0b; border: none; color: white; }
        .btn-danger { background-color: #ef4444; border: none; }
        .badge-grade { padding: 5px 12px; border-radius: 20px; font-weight: 600; }
        .grade-high { background: #dcfce7; color: #166534; }
        .grade-low { background: #fee2e2; color: #991b1b; }
    </style>
</head>
"""

@app.route('/')
def home():
    return redirect(url_for('list_students'))

# -------------------------------
# VIEW STUDENTS
# -------------------------------
@app.route('/students')
def list_students():
    avg_grade = sum(s['grade'] for s in students) / len(students) if students else 0
    
    html = f"""
    <!doctype html>
    <html lang="en">
    {BASE_HEAD}
    <body>
        <nav class="navbar navbar-expand-lg navbar-light py-3">
          <div class="container">
            <a class="navbar-brand d-flex align-items-center" href="/students">
                <i data-lucide="graduation-cap" class="me-2"></i> EduFlow
            </a>
          </div>
        </nav>

        <div class="container mt-4">
            <div class="row mb-4">
                <div class="col-md-4">
                    <div class="card stats-card p-3 mb-3">
                        <small class="text-muted text-uppercase fw-bold">Total Students</small>
                        <h2 class="mb-0 fw-bold">{{{{ students|length }}}}</h2>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card stats-card p-3 mb-3" style="border-left-color: #10b981;">
                        <small class="text-muted text-uppercase fw-bold">Average Grade</small>
                        <h2 class="mb-0 fw-bold">{avg_grade:.1f}</h2>
                    </div>
                </div>
                <div class="col-md-4 d-flex align-items-center justify-content-md-end">
                    <a href="/add_student_form" class="btn btn-primary d-flex align-items-center">
                        <i data-lucide="plus" class="me-2"></i> Add New Student
                    </a>
                </div>
            </div>

            <div class="card">
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead>
                                <tr>
                                    <th class="ps-4">ID</th>
                                    <th>Student Name</th>
                                    <th>Grade</th>
                                    <th>Section</th>
                                    <th class="text-end pe-4">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                            {% for s in students %}
                                <tr>
                                    <td class="ps-4 text-muted">#{{ s.id }}</td>
                                    <td><span class="fw-bold">{{ s.name }}</span></td>
                                    <td>
                                        <span class="badge-grade {{ 'grade-high' if s.grade >= 75 else 'grade-low' }}">
                                            {{ s.grade }}%
                                        </span>
                                    </td>
                                    <td><span class="text-secondary">{{ s.section }}</span></td>
                                    <td class="text-end pe-4">
                                        <a class="btn btn-sm btn-warning me-1" href="/edit_student/{{s.id}}">
                                            <i data-lucide="edit-3" style="width:16px;"></i>
                                        </a>
                                        <a class="btn btn-sm btn-danger" href="/delete_student/{{s.id}}" onclick="return confirm('Delete this student?')">
                                            <i data-lucide="trash-2" style="width:16px;"></i>
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <script>lucide.createIcons();</script>
    </body>
    </html>
    """
    return render_template_string(html, students=students)

# -------------------------------
# ADD STUDENT FORM
# -------------------------------
@app.route('/add_student_form')
def add_student_form():
    html = f"""
    <!doctype html>
    <html>
    {BASE_HEAD}
    <body>
        <div class="container mt-5">
            <div class="card shadow mx-auto" style="max-width: 450px;">
                <div class="card-body p-4">
                    <h3 class="fw-bold mb-4 text-center">New Student</h3>
                    <form method="POST" action="/add_student">
                        <div class="mb-3">
                            <label class="form-label text-muted small fw-bold">FULL NAME</label>
                            <input type="text" name="name" class="form-control form-control-lg" placeholder="John Doe" required>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label text-muted small fw-bold">GRADE</label>
                                <input type="number" name="grade" class="form-control form-control-lg" placeholder="0-100" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label text-muted small fw-bold">SECTION</label>
                                <input type="text" name="section" class="form-control form-control-lg" placeholder="A, B, etc." required>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary w-100 py-3 mt-2">Create Record</button>
                    </form>
                    <div class="text-center mt-4">
                        <a href="/students" class="text-decoration-none text-muted small">← Cancel and go back</a>
                    </div>
                </div>
            </div>
        </div>
        <script>lucide.createIcons();</script>
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

    html = f"""
    <!doctype html>
    <html>
    {BASE_HEAD}
    <body>
        <div class="container mt-5">
            <div class="card shadow mx-auto" style="max-width: 450px;">
                <div class="card-body p-4">
                    <h3 class="fw-bold mb-4 text-center">Update Student</h3>
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label text-muted small fw-bold">FULL NAME</label>
                            <input type="text" name="name" class="form-control form-control-lg" value="{{{{student.name}}}}" required>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label text-muted small fw-bold">GRADE</label>
                                <input type="number" name="grade" class="form-control form-control-lg" value="{{{{student.grade}}}}" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label text-muted small fw-bold">SECTION</label>
                                <input type="text" name="section" class="form-control form-control-lg" value="{{{{student.section}}}}" required>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-warning w-100 py-3 mt-2">Save Changes</button>
                    </form>
                    <div class="text-center mt-4">
                        <a href="/students" class="text-decoration-none text-muted small">← Cancel</a>
                    </div>
                </div>
            </div>
        </div>
        <script>lucide.createIcons();</script>
    </body>
    </html>
    """
    return render_template_string(html, student=student)

@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        name = request.form.get("name")
        grade = int(request.form.get("grade"))
        section = request.form.get("section")
        new_student = {
            "id": max([s["id"] for s in students]) + 1 if students else 1,
            "name": name, "grade": grade, "section": section
        }
        students.append(new_student)
    except:
        return "Error adding student"
    return redirect(url_for('list_students'))

@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('list_students'))

@app.route('/api/students')
def api_students():
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
