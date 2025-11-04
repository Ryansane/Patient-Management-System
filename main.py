from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'replace_this_with_a_strong_secret_in_prod'

db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    condition = db.Column(db.String(250), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

def add_notification(msg):
    # session-based notifications list
    notes = session.get('notifications', [])
    notes.insert(0, msg)  # newest first
    session['notifications'] = notes

def pop_notifications():
    notes = session.pop('notifications', [])
    return notes

def greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    if 12 <= hour < 17:
        return "Good afternoon"
    return "Good evening"

@app.route('/')
def dashboard():
    greet = greeting()
    notifications = session.get('notifications', [])
    return render_template('dashboard.html', greeting=greet, notifications=notifications)

# Patients CRUD
@app.route('/patients')
def patients():
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    notifications = session.get('notifications', [])
    return render_template('patients.html', patients=patients, notifications=notifications)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form.get('name')
    age = request.form.get('age', type=int)
    gender = request.form.get('gender')
    condition = request.form.get('condition')
    if not name or age is None or not gender:
        add_notification("Failed to add patient: missing fields.")
        return redirect(url_for('patients'))
    p = Patient(name=name, age=age, gender=gender, condition=condition)
    db.session.add(p)
    db.session.commit()
    add_notification(f"New patient added: {name}.")
    return redirect(url_for('patients'))

@app.route('/edit_patient/<int:id>', methods=['POST'])
def edit_patient(id):
    p = Patient.query.get_or_404(id)
    p.name = request.form.get('name')
    p.age = request.form.get('age', type=int)
    p.gender = request.form.get('gender')
    p.condition = request.form.get('condition')
    db.session.commit()
    add_notification(f"Patient updated: {p.name}.")
    return redirect(url_for('patients'))

@app.route('/delete_patient/<int:id>', methods=['POST'])
def delete_patient(id):
    p = Patient.query.get_or_404(id)
    name = p.name
    db.session.delete(p)
    db.session.commit()
    add_notification(f"Patient deleted: {name}.")
    return redirect(url_for('patients'))

@app.route('/appointments')
def appointments():
    notifications = session.get('notifications', [])
    return render_template('appointments.html', notifications=notifications)

@app.route('/billing')
def billing():
    notifications = session.get('notifications', [])
    return render_template('billing.html', notifications=notifications)

# Clear notifications endpoint (for demo)
@app.route('/clear_notifications', methods=['POST'])
def clear_notifications():
    session.pop('notifications', None)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')