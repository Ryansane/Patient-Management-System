from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            diagnosis TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- HTML TEMPLATE ---
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Patient Management System</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input, button { padding: 10px; margin: 5px; inline-size: 250px ; }
        table { inline-size: 80% ; border-collapse: collapse; margin-block-start: 20px ; }
        th, td { border: 1px solid #aaa; padding: 10px; text-align: start ; }
        h2 { margin-block-end: 10px ; }
    </style>
</head>
<body>

<h2>✅ Patient Management System</h2>

<form method="POST" action="/add">
    <input name="name" placeholder="Patient Name" required><br>
    <input name="age" placeholder="Age" type="number"><br>
    <input name="diagnosis" placeholder="Diagnosis"><br>
    <button type="submit">Add Patient</button>
</form>

<h3>📋 Patient List</h3>
<table>
    <tr><th>Name</th><th>Age</th><th>Diagnosis</th><th>Action</th></tr>
    {% for p in patients %}
    <tr>
        <td>{{ p[1] }}</td>
        <td>{{ p[2] }}</td>
        <td>{{ p[3] }}</td>
        <td><a href="/delete/{{ p[0] }}">Delete</a></td>
    </tr>
    {% endfor %}
</table>

</body>
</html>
"""

# --- ROUTES ---
@app.route('/')
def home():
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    patients = c.fetchall()
    conn.close()
    return render_template_string(HTML, patients=patients)

@app.route('/add', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form.get('age')
    diagnosis = request.form.get('diagnosis')

    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute("INSERT INTO patients (name, age, diagnosis) VALUES (?, ?, ?)",
              (name, age, diagnosis))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete_patient(id):
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute("DELETE FROM patients WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
