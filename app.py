from flask import Flask, jsonify, request, render_template_string, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "edu_flow_secret_key"  # Required for flash messages

# Sample data
students = [
    {"id": 1, "name": "Juan Dela Cruz", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria Clara", "grade": 92, "section": "Zechariah"},
    {"id": 3, "name": "Pedro Penduko", "grade": 72, "section": "Zion"},
    {"id": 4, "name": "Liza Soberano", "grade": 95, "section": "Zion"}
]

# Shared Header & Styles
BASE_HEAD = """
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>EduFlow Pro | Management</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg: #f8fafc;
            --card-bg: rgba(255, 255, 255, 0.9);
        }
        body { 
            background-color: var(--bg); 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            color: #1e293b;
            padding-top: 80px;
        }
        .glass-nav {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(226, 232, 240, 0.8);
        }
        .navbar-brand { font-weight: 800; color: var(--primary) !important; font-size: 1.5rem; }
        
        .card { 
            border: 1px solid rgba(226, 232, 240, 0.6); 
            border-radius: 16px; 
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
            background: var(--card-bg);
        }
        
        .stat-icon {
            width: 48px; height: 48px;
            display: flex; align-items: center; justify-content: center;
            border-radius: 12px; margin-bottom: 10px;
        }

        .table thead th { 
            background: #f1f5f9; 
            text-transform: uppercase; 
            font-size: 0.75rem; 
            letter-spacing: 0.05em;
            color: #64748b;
            padding: 15px;
        }

        .btn-primary { 
            background: var(--primary); border: none; font-weight: 600; 
            border-radius: 10px; padding: 10px 24px; transition: all 0.3s;
        }
        .btn-primary:hover { background: var(--primary-hover); transform: translateY(-1px); }
        
        .search-input {
            border-radius: 10px; border: 1px solid #e2e8f0; padding-left: 40px;
        }
        .search-container { position: relative; }
        .search-container i { position: absolute; left: 12px; top: 10px; color: #94a3b8; }

        .badge-status {
            padding: 6px 12px; border-radius: 8px; font-weight: 600; font-size: 0.8rem;
        }
        .status-pass { background: #dcfce7; color: #166534; }
        .status-fail { background: #fee2e2; color: #991b1b; }
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
    total = len(students)
    avg = sum(s['grade'] for s in students) / total if total > 0 else 0
    
    html = f"""
    <!doctype html>
    <html lang="en">
    {BASE_HEAD}
    <body>
        <nav class="navbar navbar-expand-lg fixed-top glass-nav">
          <div class="container">
            <a class="navbar-brand d-flex align-items-center" href="/students">
                <i data-lucide="zap" class="me-2 text-primary"></i> EduFlow Pro
            </a>
          </div>
        </nav>

        <div class="container">
            {% with messages = get_flashed_messages() %}
              {% if messages %}
                {% for message in messages %}
                  <div class="alert alert-success alert-dismissible fade show border-0 shadow-sm mb-4" role="alert" style="border-radius: 12px;">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                  </div>
                {% endfor %}
              {% endif %}
            {% endwith %}

            <div class="row align-items-end mb-4">
                <div class="col-lg-8">
                    <div class="row">
                        <div class="col-md-4">
                            <div class="card p-3 mb-3 mb-md-0">
                                <div class="stat-icon bg-primary bg-opacity-10 text-primary">
                                    <i data-lucide="users"></i>
                                </div>
                                <small class="text-muted fw-semibold">TOTAL STUDENTS</small>
                                <h3 class="fw-bold mb-0">{total}</h3>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card p-3 mb-3 mb-md-0">
                                <div class="stat-icon bg-success bg-opacity-10 text-success">
                                    <i data-lucide="trending-up"></i>
                                </div>
                                <small class="text-muted fw-semibold">AVG. PERFORMANCE</small>
                                <h3 class="fw-bold mb-0">{avg:.1f}%</h3>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 text-lg-end mt-3 mt-lg-0">
                    <a href="/add_student_form" class="btn btn-primary">
                        <i data-lucide="plus" class="me-1" style="width:18px;"></i> Add Student
                    </a>
                </div>
            </div>

            <div class="card overflow-hidden">
                <div class="card-header bg-white py-3 border-0">
                    <div class="search-container">
                        <i data-lucide="search" style="width:18px;"></i>
                        <input type="text" id="studentSearch" class="form-control search-input" placeholder="Search by name or section...">
                    </div>
                </div>
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0" id="studentTable">
                        <thead>
                            <tr>
                                <th class="ps-4">UID</th>
                                <th>Student Information</th>
                                <th>Grade</th>
                                <th>Section</th>
                                <th>Status</th>
                                <th class="text-end pe-4">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                        {% for s in students %}
                            <tr>
                                <td class="ps-4 text-muted small">#STUD-{{ s.id }}</td>
                                <td>
                                    <div class="fw-bold text-dark">{{ s.name }}</div>
                                    <div class="text-muted x-small" style="font-size: 0.75rem;">Registered Student</div>
                                </td>
                                <td>
                                    <div class="fw-semibold text-primary">{{ s.grade }}%</div>
                                    <div class="progress mt-1" style="height: 4px; width: 60px;">
                                        <div class="progress-bar bg-primary" style="width: {{ s.grade }}%"></div>
                                    </div>
                                </td>
                                <td><span class="badge bg-light text-dark border">{{ s.section }}</span></td>
                                <td>
                                    <span class="badge-status {{ 'status-pass' if s.grade >= 75 else 'status-fail' }}">
                                        {{ 'Passed' if s.grade >= 75 else 'Failed' }}
                                    </span>
                                </td>
                                <td class="text-end pe-4">
                                    <a class="btn btn-light btn-sm rounded-3 border me-1" href="/edit_student/{{s.id}}">
                                        <i data-lucide="pencil" style="width:14px;" class="text-warning"></i>
                                    </a>
                                    <a class="btn btn-light btn-sm rounded-3 border" href="/delete_student/{{s.id}}" onclick="return confirm('Archive this record?')">
                                        <i data-lucide="trash" style="width:14px;" class="text-danger"></i>
                                    </a>
                                </td>
                            </tr>
                        {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            lucide.createIcons();
            
            // Real-time Search Logic
            document.getElementById('studentSearch').addEventListener('keyup', function() {{
                let filter = this.value.toLowerCase();
                let rows = document.querySelectorAll('#studentTable tbody tr');
                rows.forEach(row => {{
                    let text = row.innerText.toLowerCase();
                    row.style.display = text.includes(filter) ? '' : 'none';
                }});
            }});
        </script>
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
    <html>{BASE_HEAD}
    <body class="d-flex align-items-center justify-content-center" style="min-height: 100vh; padding: 0;">
        <div class="container">
            <div class="card shadow-lg mx-auto border-0" style="max-width: 480px;">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <div class="stat-icon bg-primary bg-opacity-10 text-primary mx-auto">
                            <i data-lucide="user-plus"></i>
                        </div>
                        <h3 class="fw-bold mt-2">New Student</h3>
                        <p class="text-muted">Enter details to register a new student</p>
                    </div>
                    <form method="POST" action="/add_student">
                        <div class="mb-3">
                            <label class="form-label small fw-bold text-uppercase">Full Name</label>
                            <input type="text" name="name" class="form-control py-2 shadow-sm border-light-subtle" placeholder="e.g. John Smith" required>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label small fw-bold text-uppercase">Grade (%)</label>
                                <input type="number" name="grade" class="form-control py-2 shadow-sm border-light-subtle" min="0" max="100" placeholder="85" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label small fw-bold text-uppercase">Section</label>
                                <input type="text" name="section" class="form-control py-2 shadow-sm border-light-subtle" placeholder="A1" required>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary w-100 py-3 mt-3 shadow">Create Record</button>
                        <a href="/students" class="btn btn-link w-100 mt-2 text-muted text-decoration-none small">Cancel</a>
                    </form>
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
    if not student: return "Student not found", 404

    if request.method == 'POST':
        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]
        flash(f"Record for {student['name']} updated successfully!")
        return redirect(url_for('list_students'))

    html = f"""
    <!doctype html>
    <html>{BASE_HEAD}
    <body class="d-flex align-items-center justify-content-center" style="min-height: 100vh; padding: 0;">
        <div class="container">
            <div class="card shadow-lg mx-auto border-0" style="max-width: 480px;">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <div class="stat-icon bg-warning bg-opacity-10 text-warning mx-auto">
                            <i data-lucide="edit-2"></i>
                        </div>
                        <h3 class="fw-bold mt-2">Update Record</h3>
                        <p class="text-muted">Modifying ID: #{{{{ student.id }}}}</p>
                    </div>
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label small fw-bold text-uppercase">Full Name</label>
                            <input type="text" name="name" class="form-control py-2 shadow-sm" value="{{{{student.name}}}}" required>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label small fw-bold text-uppercase">Grade (%)</label>
                                <input type="number" name="grade" class="form-control py-2 shadow-sm" value="{{{{student.grade}}}}" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label small fw-bold text-uppercase">Section</label>
                                <input type="text" name="section" class="form-control py-2 shadow-sm" value="{{{{student.section}}}}" required>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary w-100 py-3 mt-3 shadow">Save Changes</button>
                        <a href="/students" class="btn btn-link w-100 mt-2 text-muted text-decoration-none small">Cancel</a>
                    </form>
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
        new_id = max([s["id"] for s in students]) + 1 if students else 1
        students.append({"id": new_id, "name": name, "grade": grade, "section": section})
        flash(f"Student {name} added to the database.")
    except:
        return "Error adding student"
    return redirect(url_for('list_students'))

@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    flash("Record removed successfully.")
    return redirect(url_for('list_students'))

if __name__ == '__main__':
    app.run(debug=True)
