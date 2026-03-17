from flask import Flask, jsonify, request, render_template_string, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Sample data with more fields
students = [
    {"id": 1, "name": "Juan Dela Cruz", "grade": 85, "section": "Zechariah", "email": "juan@school.edu", "created_at": "2024-01-15"},
    {"id": 2, "name": "Maria Santos", "grade": 90, "section": "Zechariah", "email": "maria@school.edu", "created_at": "2024-01-16"},
    {"id": 3, "name": "Pedro Reyes", "grade": 70, "section": "Zion", "email": "pedro@school.edu", "created_at": "2024-01-17"},
    {"id": 4, "name": "Ana Garcia", "grade": 95, "section": "Zephaniah", "email": "ana@school.edu", "created_at": "2024-01-18"},
    {"id": 5, "name": "Carlos Rivera", "grade": 78, "section": "Zion", "email": "carlos@school.edu", "created_at": "2024-01-19"},
]

# Predefined sections
SECTIONS = ["Zechariah", "Zion", "Zephaniah", "Zadok", "Zebulun"]

def get_grade_color(grade):
    """Return color class based on grade."""
    if grade >= 90:
        return "success"
    elif grade >= 80:
        return "primary"
    elif grade >= 75:
        return "warning"
    else:
        return "danger"

def get_stats():
    """Calculate statistics."""
    if not students:
        return {"total": 0, "avg": 0, "highest": 0, "lowest": 0, "passing": 0}
    
    grades = [s["grade"] for s in students]
    passing = len([g for g in grades if g >= 75])
    return {
        "total": len(students),
        "avg": round(sum(grades) / len(grades), 1),
        "highest": max(grades),
        "lowest": min(grades),
        "passing": passing,
        "passing_rate": round((passing / len(students)) * 100, 1)
    }

# Base template with modern UI
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-bs-theme="light">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title }} | Student Manager</title>
    <link href="[cdn.jsdelivr.net](https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css)" rel="stylesheet">
    <link href="[cdn.jsdelivr.net](https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css)" rel="stylesheet">
    <style>
        :root {
            --gradient-start: #667eea;
            --gradient-end: #764ba2;
        }
        
        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }
        
        .navbar {
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)) !important;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        }
        
        .navbar-brand {
            font-weight: 700;
            font-size: 1.4rem;
            letter-spacing: -0.5px;
        }
        
        .stat-card {
            border: none;
            border-radius: 16px;
            transition: all 0.3s ease;
            overflow: hidden;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.12);
        }
        
        .stat-card .card-body {
            padding: 1.5rem;
        }
        
        .stat-icon {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: 700;
            line-height: 1.2;
        }
        
        .stat-label {
            color: #6c757d;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .main-card {
            border: none;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            overflow: hidden;
        }
        
        .card-header-custom {
            background: white;
            border-bottom: 1px solid #eee;
            padding: 1.25rem 1.5rem;
        }
        
        .table {
            margin-bottom: 0;
        }
        
        .table thead th {
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.5px;
            padding: 1rem;
            border: none;
        }
        
        .table tbody td {
            padding: 1rem;
            vertical-align: middle;
            border-color: #f0f0f0;
        }
        
        .table tbody tr {
            transition: all 0.2s ease;
        }
        
        .table tbody tr:hover {
            background-color: #f8f9ff;
        }
        
        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.9rem;
            color: white;
        }
        
        .grade-badge {
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
        }
        
        .section-badge {
            background: #e8f4fd;
            color: #0d6efd;
            padding: 0.35rem 0.75rem;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .btn-action {
            width: 36px;
            height: 36px;
            padding: 0;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            transition: all 0.2s ease;
        }
        
        .btn-action:hover {
            transform: scale(1.1);
        }
        
        .btn-gradient {
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
            border: none;
            color: white;
            padding: 0.6rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .btn-gradient:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            color: white;
        }
        
        .form-card {
            border: none;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .form-header {
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
            padding: 2rem;
            text-align: center;
            color: white;
        }
        
        .form-header i {
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.9;
        }
        
        .form-control, .form-select {
            border-radius: 12px;
            padding: 0.75rem 1rem;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
        }
        
        .form-control:focus, .form-select:focus {
            border-color: var(--gradient-start);
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }
        
        .form-label {
            font-weight: 600;
            color: #495057;
            margin-bottom: 0.5rem;
        }
        
        .search-box {
            position: relative;
        }
        
        .search-box i {
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: #adb5bd;
        }
        
        .search-box input {
            padding-left: 2.75rem;
        }
        
        .empty-state {
            padding: 4rem 2rem;
            text-align: center;
        }
        
        .empty-state i {
            font-size: 4rem;
            color: #dee2e6;
            margin-bottom: 1rem;
        }
        
        .toast-container {
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 1050;
        }
        
        @media (max-width: 768px) {
            .stat-card .stat-value {
                font-size: 1.4rem;
            }
            .table-responsive {
                font-size: 0.9rem;
            }
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark sticky-top">
        <div class="container">
            <a class="navbar-brand" href="/students">
                <i class="bi bi-mortarboard-fill me-2"></i>Student Manager
            </a>
            <div class="d-flex align-items-center">
                <a href="/students" class="btn btn-outline-light btn-sm me-2 {{ 'active' if active_page == 'list' else '' }}">
                    <i class="bi bi-list-ul me-1"></i>Students
                </a>
                <a href="/add_student_form" class="btn btn-light btn-sm">
                    <i class="bi bi-plus-lg me-1"></i>Add New
                </a>
            </div>
        </div>
    </nav>
    
    <div class="toast-container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                <div class="toast show align-items-center text-white bg-{{ category }} border-0" role="alert">
                    <div class="d-flex">
                        <div class="toast-body">
                            <i class="bi bi-{{ 'check-circle' if category == 'success' else 'exclamation-circle' }} me-2"></i>
                            {{ message }}
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                    </div>
                </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>
    
    <main class="container py-4">
        {% block content %}{% endblock %}
    </main>
    
    <footer class="text-center py-4 text-muted">
        <small>&copy; 2024 Student Manager. Built with Flask & Bootstrap.</small>
    </footer>
    
    <script src="[cdn.jsdelivr.net](https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js)"></script>
    <script>
        // Auto-hide toasts
        document.querySelectorAll('.toast').forEach(toast => {
            setTimeout(() => toast.classList.remove('show'), 4000);
        });
        
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                const filter = this.value.toLowerCase();
                document.querySelectorAll('tbody tr').forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(filter) ? '' : 'none';
                });
            });
        }
    </script>
</body>
</html>
"""

# -------------------------------
# HOME REDIRECT
# -------------------------------
@app.route('/')
def home():
    return redirect(url_for('list_students'))

# -------------------------------
# VIEW STUDENTS
# -------------------------------
@app.route('/students')
def list_students():
    stats = get_stats()
    html = """
    {% extends base %}
    {% block content %}
    <!-- Stats Row -->
    <div class="row g-3 mb-4">
        <div class="col-6 col-lg-3">
            <div class="stat-card card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <div class="stat-value text-primary">{{ stats.total }}</div>
                            <div class="stat-label">Total Students</div>
                        </div>
                        <div class="stat-icon bg-primary bg-opacity-10 text-primary">
                            <i class="bi bi-people"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-6 col-lg-3">
            <div class="stat-card card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <div class="stat-value text-success">{{ stats.avg }}</div>
                            <div class="stat-label">Average Grade</div>
                        </div>
                        <div class="stat-icon bg-success bg-opacity-10 text-success">
                            <i class="bi bi-graph-up"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-6 col-lg-3">
            <div class="stat-card card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <div class="stat-value text-warning">{{ stats.highest }}</div>
                            <div class="stat-label">Highest Grade</div>
                        </div>
                        <div class="stat-icon bg-warning bg-opacity-10 text-warning">
                            <i class="bi bi-trophy"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-6 col-lg-3">
            <div class="stat-card card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <div class="stat-value text-info">{{ stats.passing_rate }}%</div>
                            <div class="stat-label">Passing Rate</div>
                        </div>
                        <div class="stat-icon bg-info bg-opacity-10 text-info">
                            <i class="bi bi-check-circle"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Main Table Card -->
    <div class="main-card card">
        <div class="card-header-custom">
            <div class="row align-items-center">
                <div class="col-md-6 mb-3 mb-md-0">
                    <h5 class="mb-0 fw-bold">
                        <i class="bi bi-table me-2 text-primary"></i>Student Directory
                    </h5>
                </div>
                <div class="col-md-6">
                    <div class="d-flex gap-2 justify-content-md-end">
                        <div class="search-box flex-grow-1" style="max-width: 300px;">
                            <i class="bi bi-search"></i>
                            <input type="text" id="searchInput" class="form-control" placeholder="Search students...">
                        </div>
                        <a href="/add_student_form" class="btn btn-gradient">
                            <i class="bi bi-plus-lg me-1"></i>Add
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        {% if students %}
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Student</th>
                        <th>Email</th>
                        <th class="text-center">Grade</th>
                        <th class="text-center">Section</th>
                        <th class="text-center">Actions</th>
                    </tr>
                </thead>
                <tbody>
                {% for s in students %}
                    <tr>
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="avatar me-3" style="background: linear-gradient(135deg, {{ ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'][s.id % 5] }}, {{ ['#764ba2', '#667eea', '#f5576c', '#f093fb', '#00f2fe'][s.id % 5] }});">
                                    {{ s.name[0] }}
                                </div>
                                <div>
                                    <div class="fw-semibold">{{ s.name }}</div>
                                    <small class="text-muted">ID: {{ s.id }}</small>
                                </div>
                            </div>
                        </td>
                        <td>
                            <i class="bi bi-envelope text-muted me-1"></i>
                            {{ s.email or 'N/A' }}
                        </td>
                        <td class="text-center">
                            <span class="grade-badge bg-{{ get_grade_color(s.grade) }} bg-opacity-10 text-{{ get_grade_color(s.grade) }}">
                                {{ s.grade }}%
                            </span>
                        </td>
                        <td class="text-center">
                            <span class="section-badge">{{ s.section }}</span>
                        </td>
                        <td class="text-center">
                            <a href="/view_student/{{ s.id }}" class="btn btn-action btn-outline-info me-1" title="View">
                                <i class="bi bi-eye"></i>
                            </a>
                            <a href="/edit_student/{{ s.id }}" class="btn btn-action btn-outline-warning me-1" title="Edit">
                                <i class="bi bi-pencil"></i>
                            </a>
                            <a href="/delete_student/{{ s.id }}" class="btn btn-action btn-outline-danger" title="Delete" 
                               onclick="return confirm('Are you sure you want to delete {{ s.name }}?')">
                                <i class="bi bi-trash"></i>
                            </a>
                        </td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <div class="empty-state">
            <i class="bi bi-inbox"></i>
            <h4 class="text-muted">No Students Found</h4>
            <p class="text-muted mb-4">Get started by adding your first student.</p>
            <a href="/add_student_form" class="btn btn-gradient">
                <i class="bi bi-plus-lg me-2"></i>Add Student
            </a>
        </div>
        {% endif %}
    </div>
    {% endblock %}
    """
    return render_template_string(html, base=BASE_TEMPLATE, title="Dashboard", active_page="list",
                                  students=students, stats=stats, get_grade_color=get_grade_color)

# -------------------------------
# VIEW SINGLE STUDENT
# -------------------------------
@app.route('/view_student/<int:id>')
def view_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for('list_students'))
    
    html = """
    {% extends base %}
    {% block content %}
    <div class="row justify-content-center">
        <div class="col-lg-6">
            <div class="form-card card">
                <div class="form-header">
                    <div class="avatar mx-auto mb-3" style="width: 80px; height: 80px; font-size: 2rem; background: rgba(255,255,255,0.2);">
                        {{ student.name[0] }}
                    </div>
                    <h3 class="mb-1">{{ student.name }}</h3>
                    <p class="mb-0 opacity-75">Student ID: {{ student.id }}</p>
                </div>
                <div class="card-body p-4">
                    <div class="row g-4">
                        <div class="col-6">
                            <div class="text-muted small mb-1">Email</div>
                            <div class="fw-semibold">
                                <i class="bi bi-envelope me-2 text-primary"></i>{{ student.email or 'N/A' }}
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="text-muted small mb-1">Section</div>
                            <div class="fw-semibold">
                                <i class="bi bi-collection me-2 text-primary"></i>{{ student.section }}
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="text-muted small mb-1">Grade</div>
                            <div>
                                <span class="grade-badge bg-{{ get_grade_color(student.grade) }} bg-opacity-10 text-{{ get_grade_color(student.grade) }}">
                                    {{ student.grade }}%
                                </span>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="text-muted small mb-1">Status</div>
                            <div>
                                {% if student.grade >= 75 %}
                                <span class="badge bg-success"><i class="bi bi-check-circle me-1"></i>Passing</span>
                                {% else %}
                                <span class="badge bg-danger"><i class="bi bi-x-circle me-1"></i>Failing</span>
                                {% endif %}
                            </div>
                        </div>
                        <div class="col-12">
                            <div class="text-muted small mb-1">Enrolled Since</div>
                            <div class="fw-semibold">
                                <i class="bi bi-calendar me-2 text-primary"></i>{{ student.created_at or 'N/A' }}
                            </div>
                        </div>
                    </div>
                    
                    <hr class="my-4">
                    
                    <div class="d-flex gap-2">
                        <a href="/edit_student/{{ student.id }}" class="btn btn-warning flex-fill">
                            <i class="bi bi-pencil me-2"></i>Edit
                        </a>
                        <a href="/delete_student/{{ student.id }}" class="btn btn-outline-danger" 
                           onclick="return confirm('Delete this student?')">
                            <i class="bi bi-trash"></i>
                        </a>
                    </div>
                    
                    <div class="text-center mt-3">
                        <a href="/students" class="text-decoration-none">
                            <i class="bi bi-arrow-left me-1"></i>Back to List
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(html, base=BASE_TEMPLATE, title=f"View {student['name']}", 
                                  active_page="view", student=student, get_grade_color=get_grade_color)

# -------------------------------
# ADD STUDENT FORM
# -------------------------------
@app.route('/add_student_form')
def add_student_form():
    html = """
    {% extends base %}
    {% block content %}
    <div class="row justify-content-center">
        <div class="col-lg-5">
            <div class="form-card card">
                <div class="form-header">
                    <i class="bi bi-person-plus"></i>
                    <h3 class="mb-1">Add New Student</h3>
                    <p class="mb-0 opacity-75">Fill in the details below</p>
                </div>
                <div class="card-body p-4">
                    <form method="POST" action="/add_student" id="studentForm">
                        <div class="mb-3">
                            <label class="form-label">
                                <i class="bi bi-person me-1"></i>Full Name
                            </label>
                            <input type="text" name="name" class="form-control" placeholder="Enter student name" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">
                                <i class="bi bi-envelope me-1"></i>Email Address
                            </label>
                            <input type="email" name="email" class="form-control" placeholder="student@school.edu">
                        </div>
                        <div class="row">
                            <div class="col-6 mb-3">
                                <label class="form-label">
                                    <i class="bi bi-percent me-1"></i>Grade
                                </label>
                                <input type="number" name="grade" class="form-control" min="0" max="100" placeholder="0-100" required>
                            </div>
                            <div class="col-6 mb-3">
                                <label class="form-label">
                                    <i class="bi bi-collection me-1"></i>Section
                                </label>
                                <select name="section" class="form-select" required>
                                    <option value="">Select...</option>
                                    {% for section in sections %}
                                    <option value="{{ section }}">{{ section }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                        </div>
                        <div class="d-grid gap-2 mt-4">
                            <button type="submit" class="btn btn-gradient btn-lg">
                                <i class="bi bi-check-lg me-2"></i>Add Student
                            </button>
                            <a href="/students" class="btn btn-outline-secondary">
                                <i class="bi bi-x-lg me-2"></i>Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(html, base=BASE_TEMPLATE, title="Add Student", 
                                  active_page="add", sections=SECTIONS)

# -------------------------------
# EDIT STUDENT FORM
# -------------------------------
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for('list_students'))

    if request.method == 'POST':
        student["name"] = request.form.get("name", "").strip()
        student["email"] = request.form.get("email", "").strip()
        student["grade"] = int(request.form.get("grade", 0))
        student["section"] = request.form.get("section", "")
        flash(f"Successfully updated {student['name']}!", "success")
        return redirect(url_for('list_students'))

    html = """
    {% extends base %}
    {% block content %}
    <div class="row justify-content-center">
        <div class="col-lg-5">
            <div class="form-card card">
                <div class="form-header" style="background: linear-gradient(135deg, #f5af19, #f12711);">
                    <i class="bi bi-pencil-square"></i>
                    <h3 class="mb-1">Edit Student</h3>
                    <p class="mb-0 opacity-75">Update student information</p>
                </div>
                <div class="card-body p-4">
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">
                                <i class="bi bi-person me-1"></i>Full Name
                            </label>
                            <input type="text" name="name" class="form-control" value="{{ student.name }}" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">
                                <i class="bi bi-envelope me-1"></i>Email Address
                            </label>
                            <input type="email" name="email" class="form-control" value="{{ student.email or '' }}">
                        </div>
                        <div class="row">
                            <div class="col-6 mb-3">
                                <label class="form-label">
                                    <i class="bi bi-percent me-1"></i>Grade
                                </label>
                                <input type="number" name="grade" class="form-control" min="0" max="100" value="{{ student.grade }}" required>
                            </div>
                            <div class="col-6 mb-3">
                                <label class="form-label">
                                    <i class="bi bi-collection me-1"></i>Section
                                </label>
                                <select name="section" class="form-select" required>
                                    {% for section in sections %}
                                    <option value="{{ section }}" {{ 'selected' if section == student.section else '' }}>{{ section }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                        </div>
                        <div class="d-grid gap-2 mt-4">
                            <button type="submit" class="btn btn-warning btn-lg">
                                <i class="bi bi-check-lg me-2"></i>Update Student
                            </button>
                            <a href="/students" class="btn btn-outline-secondary">
                                <i class="bi bi-x-lg me-2"></i>Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(html, base=BASE_TEMPLATE, title=f"Edit {student['name']}", 
                                  active_page="edit", student=student, sections=SECTIONS)

# -------------------------------
# ADD STUDENT (POST)
# -------------------------------
@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        grade = int(request.form.get("grade", 0))
        section = request.form.get("section", "")
        
        if not name or not section:
            flash("Name and section are required.", "danger")
            return redirect(url_for('add_student_form'))
        
        if grade < 0 or grade > 100:
            flash("Grade must be between 0 and 100.", "danger")
            return redirect(url_for('add_student_form'))
        
        new_student = {
            "id": max([s["id"] for s in students], default=0) + 1,
            "name": name,
            "email": email,
            "grade": grade,
            "section": section,
            "created_at": datetime.now().strftime("%Y-%m-%d")
        }
        students.append(new_student)
        flash(f"Successfully added {name}!", "success")
    except ValueError:
        flash("Invalid grade value.", "danger")
        return redirect(url_for('add_student_form'))
    except Exception as e:
        flash(f"Error adding student: {str(e)}", "danger")
        return redirect(url_for('add_student_form'))
    
    return redirect(url_for('list_students'))

# -------------------------------
# DELETE STUDENT
# -------------------------------
@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    student = next((s for s in students if s["id"] == id), None)
    if student:
        name = student["name"]
        students = [s for s in students if s["id"] != id]
        flash(f"Successfully deleted {name}.", "success")
    else:
        flash("Student not found.", "danger")
    return redirect(url_for('list_students'))

# -------------------------------
# API ENDPOINTS
# -------------------------------
@app.route('/api/students', methods=['GET'])
def api_get_students():
    """Get all students."""
    return jsonify({
        "success": True,
        "data": students,
        "count": len(students)
    })

@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    """Get a single student by ID."""
    student = next((s for s in students if s["id"] == id), None)
    if student:
        return jsonify({"success": True, "data": student})
    return jsonify({"success": False, "error": "Student not found"}), 404

@app.route('/api/students', methods=['POST'])
def api_add_student():
    """Add a new student via API."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    
    required = ["name", "grade", "section"]
    for field in required:
        if field not in data:
            return jsonify({"success": False, "error": f"Missing field: {field}"}), 400
    
    new_student = {
        "id": max([s["id"] for s in students], default=0) + 1,
        "name": data["name"],
        "email": data.get("email", ""),
        "grade": int(data["grade"]),
        "section": data["section"],
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    students.append(new_student)
    return jsonify({"success": True, "data": new_student}), 201

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get statistics."""
    return jsonify({"success": True, "data": get_stats()})

# -------------------------------
# RUN
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
