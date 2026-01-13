// Main JS - Handles AJAX and UI interactions

// --- Base URL ---
const API_BASE = '/api';

// --- Login --
async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        if (data.success) {
            window.location.href = '/dashboard';
        } else {
            alert(data.message || 'Login failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Check backend.');
    }
}

// --- Dashboard ---
async function loadStats() {
    try {
        const res = await fetch(`${API_BASE}/stats`);
        const data = await res.json();

        document.getElementById('patient-count').innerText = data.patients || 0;
        document.getElementById('doctor-count').innerText = data.doctors || 0;
        document.getElementById('appointment-count').innerText = data.appointments || 0;
    } catch (e) {
        console.log('Error loading stats', e);
    }
}

// --- Patient Management ---
async function loadPatients() {
    const res = await fetch(`${API_BASE}/patients`);
    const data = await res.json();
    const tbody = document.getElementById('patients-table-body');
    tbody.innerHTML = '';

    data.patients.forEach(p => {
        tbody.innerHTML += `
            <tr>
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>${p.age}</td>
                <td>${p.contact}</td>
                <td>${p.gender}</td>
            </tr>
        `;
    });
}

async function addPatient(event) {
    event.preventDefault();
    const form = document.getElementById('add-patient-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    const res = await fetch(`${API_BASE}/patients`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await res.json();
    if (result.success) {
        alert('Patient Added!');
        closeModal();
        loadPatients();
    } else {
        alert('Error adding patient');
    }
}

// --- Generic Helper ---
function logout() {
    fetch(`${API_BASE}/logout`, { method: 'POST' })
        .then(() => window.location.href = '/login');
}

function openModal(id) {
    document.getElementById(id).classList.add('active');
}

function closeModal() {
    document.querySelectorAll('.modal').forEach(m => m.classList.remove('active'));
}
