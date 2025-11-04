from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Secret key for sessions (use environment variable in production)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database setup - use absolute path for Render deployment
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    f'sqlite:///{os.path.join(basedir, "patients.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Patient Model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.String(20))
    phone = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dob': self.dob,
            'phone': self.phone,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
        }

# Create DB
with app.app_context():
    db.create_all()

# HTML Template
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Patient Management System</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        input, textarea { display: block; margin: 8px 0; inline-size: 300px; padding: 6px; }
        table { border-collapse: collapse; margin-block-start: 20px; inline-size: 100%; }
        td, th { border: 1px solid #ddd; padding: 8px; }
        button { padding: 6px; margin-inline-end: 5px; }
        .info-header { color: #666; font-size: 14px; margin-block-end: 10px; }
        .nav-buttons { margin-block-end: 20px; }
        .nav-buttons button { margin-inline-end: 10px; }
        .section { display: none; }
        .section.active { display: block; }
    </style>
</head>
<body>
    <div class="info-header">Ryan Sanya B141/24909/2022</div>
    <h2>✅ Patient Management System</h2>
    
    <div class="nav-buttons">
        <button onclick="showSection('patients')">Patients</button>
        <button onclick="showSection('appointments')">Appointments</button>
        <button onclick="showSection('billing')">Billing</button>
    </div>

    <!-- Patients Section -->
    <div id="patients" class="section active">
        <h3>Add New Patient</h3>
        <form id="addForm">
            <input id="first_name" placeholder="First Name" required />
            <input id="last_name" placeholder="Last Name" required />
            <input id="dob" placeholder="Date of Birth (YYYY-MM-DD)" />
            <input id="phone" placeholder="Phone Number" />
            <textarea id="notes" placeholder="Notes"></textarea>
            <button type="submit">Add Patient</button>
        </form>

        <h3>Patients</h3>
        <table id="patientsTable">
            <thead>
                <tr>
                    <th>ID</th><th>Name</th><th>DOB</th><th>Phone</th><th>Notes</th><th>Actions</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>

    <!-- Appointments Section -->
    <div id="appointments" class="section">
        <h3>Appointments</h3>
        <p>Appointment scheduling feature coming soon.</p>
    </div>

    <!-- Billing Section -->
    <div id="billing" class="section">
        <h3>Billing</h3>
        <p>Billing and invoice management feature coming soon.</p>
    </div>

<script>
async function fetchPatients() {
    const res = await fetch('/api/patients');
    const data = await res.json();
    const tbody = document.querySelector('#patientsTable tbody');
    tbody.innerHTML = '';
    data.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.id}</td>
            <td>${p.first_name} ${p.last_name}</td>
            <td>${p.dob || ''}</td>
            <td>${p.phone || ''}</td>
            <td>${p.notes || ''}</td>
            <td>
                <button onclick="deletePatient(${p.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Add Patient
document.getElementById('addForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = {
        first_name: first_name.value,
        last_name: last_name.value,
        dob: dob.value,
        phone: phone.value,
        notes: notes.value
    };

    await fetch('/api/patients', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });

    document.getElementById('addForm').reset();
    fetchPatients();
});

// Delete Patient
async function deletePatient(id) {
    await fetch(`/api/patients/${id}`, { method: 'DELETE' });
    fetchPatients();
}

fetchPatients();

// Navigation function
function showSection(sectionName) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(sectionName).classList.add('active');
}
</script>
</body>
</html>
"""

# ROUTES
@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/api/patients', methods=['GET'])
def list_patients():
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    return jsonify([p.to_dict() for p in patients])

@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.json
    p = Patient(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        dob=data.get('dob'),
        phone=data.get('phone'),
        notes=data.get('notes')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict())

@app.route('/api/patients/<int:pid>', methods=['DELETE'])
def delete_patient(pid):
    p = Patient.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
