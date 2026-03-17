import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Required for flash messages

DATA_FILE = 'students.json'

# --- Data Persistence Logic ---
def load_students():
    if not os.path.exists(DATA_FILE):
        return [
            {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
            {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"}
        ]
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_students(students):
    with open(DATA_FILE, 'w') as f:
        json.dump(students, f, indent=4)

# --- Routes ---

@app.route('/')
def index():
    return redirect(url_for('list_students'))

@app.route('/students')
def list_students():
    students = load_students()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        students = load_students()
        try:
            new_id = max([s['id'] for s in students], default=0) + 1
            new_student = {
                "id": new_id,
                "name": request.form['name'],
                "grade": int(request.form['grade']),
                "section": request.form['section']
            }
            students.append(new_student)
            save_students(students)
            flash(f"Student {new_student['name']} added!", "success")
            return redirect(url_for('list_students'))
        except ValueError:
            flash("Invalid input. Please check your data.", "danger")
            
    return render_template('form.html', title="Add Student", student=None)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    students = load_students()
    student = next((s for s in students if s['id'] == id), None)
    
    if not student:
        flash("Student not found!", "danger")
        return redirect(url_for('list_students'))

    if request.method == 'POST':
        student.update({
            "name": request.form['name'],
            "grade": int(request.form['grade']),
            "section": request.form['section']
        })
        save_students(students)
        flash("Student updated successfully!", "info")
        return redirect(url_for('list_students'))

    return render_template('form.html', title="Edit Student", student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    students = load_students()
    updated_students = [s for s in students if s['id'] != id]
    save_students(updated_students)
    flash("Student record deleted.", "warning")
    return redirect(url_for('list_students'))

if __name__ == '__main__':
    app.run(debug=True)
