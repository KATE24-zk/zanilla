from flask import Flask, render_template_string, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# -----------------------
# DATABASE CONFIG (MySQL)
# -----------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/student_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------
# MODEL
# -----------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    grade = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.String(20))

# Auto create tables
@app.before_request
def create_tables():
    db.create_all()

# -----------------------
# BASE TEMPLATE (MODERN UI)
# -----------------------
BASE = """
<!DOCTYPE html>
<html lang="en" data-bs-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{{ title }}</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">

<style>
body {
    background: linear-gradient(135deg,#1e3c72,#2a5298);
    color:white;
}
.card {
    background: rgba(255,255,255,0.08);
    border:none;
    border-radius:15px;
}
.avatar {
    width:40px;height:40px;
    border-radius:50%;
    background:#00c6ff;
    display:flex;
    align-items:center;
    justify-content:center;
}
</style>
</head>

<body>

<nav class="navbar navbar-dark bg-dark px-3">
    <a href="/students" class="navbar-brand">🎓 Student Manager</a>
    <div>
        <a href="/students" class="btn btn-light btn-sm">Students</a>
        <a href="/add" class="btn btn-success btn-sm">Add</a>
    </div>
</nav>

<div class="container py-4">
{% with messages = get_flashed_messages(with_categories=true) %}
{% for c,m in messages %}
<div class="alert alert-{{c}}">{{m}}</div>
{% endfor %}
{% endwith %}

{% block content %}{% endblock %}
</div>

</body>
</html>
"""

# -----------------------
# ROUTES
# -----------------------

@app.route('/')
def home():
    return redirect(url_for('students'))

# -----------------------
# LIST
# -----------------------
@app.route('/students')
def students():
    data = Student.query.all()
    return render_template_string("""
{% extends base %}
{% block content %}

<h3>Students</h3>

<div class="card p-3">
<table class="table text-white">
<thead>
<tr>
<th>Name</th><th>Email</th><th>Grade</th><th>Section</th><th>Action</th>
</tr>
</thead>
<tbody>

{% for s in data %}
<tr>
<td>
<div class="d-flex align-items-center">
<div class="avatar me-2">{{ s.name[0] }}</div>
{{ s.name }}
</div>
</td>

<td>{{ s.email }}</td>
<td>{{ s.grade }}</td>
<td>{{ s.section }}</td>

<td>
<a href="/edit/{{s.id}}" class="btn btn-warning btn-sm">Edit</a>
<a href="/delete/{{s.id}}" class="btn btn-danger btn-sm">Delete</a>
</td>

</tr>
{% endfor %}

</tbody>
</table>
</div>

{% endblock %}
""", base=BASE, title="Students", data=data)

# -----------------------
# ADD
# -----------------------
@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        s = Student(
            name=request.form['name'],
            email=request.form['email'],
            grade=int(request.form['grade']),
            section=request.form['section'],
            created_at=datetime.now().strftime("%Y-%m-%d")
        )
        db.session.add(s)
        db.session.commit()
        flash("Added successfully","success")
        return redirect('/students')

    return render_template_string("""
{% extends base %}
{% block content %}

<h3>Add Student</h3>

<form method="POST" class="card p-3">

<input name="name" class="form-control mb-2" placeholder="Name" required>
<input name="email" class="form-control mb-2" placeholder="Email">
<input name="grade" type="number" class="form-control mb-2" placeholder="Grade">
<input name="section" class="form-control mb-2" placeholder="Section">

<button class="btn btn-success">Save</button>

</form>

{% endblock %}
""", base=BASE)

# -----------------------
# EDIT
# -----------------------
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    s = Student.query.get(id)

    if request.method == 'POST':
        s.name = request.form['name']
        s.email = request.form['email']
        s.grade = int(request.form['grade'])
        s.section = request.form['section']
        db.session.commit()

        flash("Updated!","success")
        return redirect('/students')

    return render_template_string("""
{% extends base %}
{% block content %}

<h3>Edit Student</h3>

<form method="POST" class="card p-3">

<input name="name" value="{{s.name}}" class="form-control mb-2">
<input name="email" value="{{s.email}}" class="form-control mb-2">
<input name="grade" value="{{s.grade}}" class="form-control mb-2">
<input name="section" value="{{s.section}}" class="form-control mb-2">

<button class="btn btn-warning">Update</button>

</form>

{% endblock %}
""", base=BASE, s=s)

# -----------------------
# DELETE
# -----------------------
@app.route('/delete/<int:id>')
def delete(id):
    s = Student.query.get(id)
    db.session.delete(s)
    db.session.commit()
    flash("Deleted","danger")
    return redirect('/students')

# -----------------------
# API
# -----------------------
@app.route('/api')
def api():
    data = Student.query.all()
    return jsonify([{
        "id": s.id,
        "name": s.name,
        "grade": s.grade
    } for s in data])

# -----------------------
# RUN
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
