from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from db_config import get_db_connection
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_demo'

# --- Database Helper ---
def query_db(query, args=(), one=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
        if query.strip().upper().startswith("SELECT"):
            rv = cursor.fetchall()
            return (dict(rv[0]) if rv else None) if one else [dict(row) for row in rv]
        else:
            conn.commit()
            return cursor.lastrowid
    except Exception as err:
        print(f"Database Error: {err}")
        return None
    finally:
        conn.close()

# --- Routes: Pages ---
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login_page'))
    return render_template('dashboard.html')

@app.route('/patients')
def patients_page():
    if 'user_id' not in session: return redirect(url_for('login_page'))
    return render_template('patients.html')

@app.route('/appointments')
def appointments_page():
    if 'user_id' not in session: return redirect(url_for('login_page'))
    return render_template('appointments.html')

@app.route('/billing')
def billing_page():
    if 'user_id' not in session: return redirect(url_for('login_page'))
    return render_template('billing.html')

# --- Routes: API ---

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Simple check (In real app, use password hashing!)
    # For demo, assumes we have a user 'admin' with password 'admin123'
    # We will check database if it exists, otherwise hardcoded fallback for demo if DB fails
    
    try:
        user = query_db("SELECT * FROM users WHERE username = %s", (username,), one=True)
        if user and user['password_hash'] == password: # Plain text for simplicity in this demo step, normally hash
            session['user_id'] = user['id']
            session['username'] = user['username']
            return jsonify({'success': True})
        
        # Fallback for when DB is empty/locked
        if username == 'admin' and password == 'admin123':
             session['user_id'] = 1
             session['username'] = 'admin'
             return jsonify({'success': True})
             
    except Exception as e:
        # Fallback to allow login even if DB is broken for UI demo
        if username == 'admin' and password == 'admin123':
             session['user_id'] = 1
             session['username'] = 'admin'
             return jsonify({'success': True, 'message': 'Logged in (Offline Mode)'})

    return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/stats')
def api_stats():
    # Mock data if DB fails
    try:
        p_count = query_db("SELECT COUNT(*) as c FROM patients", one=True)['c']
        d_count = query_db("SELECT COUNT(*) as c FROM doctors", one=True)['c']
        a_count = query_db("SELECT COUNT(*) as c FROM appointments WHERE status='Scheduled'", one=True)['c']
    except:
        p_count, d_count, a_count = 0, 0, 0
        
    return jsonify({'patients': p_count, 'doctors': d_count, 'appointments': a_count})

@app.route('/api/patients', methods=['GET', 'POST'])
def api_patients():
    if request.method == 'POST':
        data = request.json
        sql = "INSERT INTO patients (name, age, gender, contact, address, medical_history) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (data['name'], data['age'], data['gender'], data['contact'], data['address'], data['history'])
        try:
            query_db(sql, val)
            return jsonify({'success': True})
        except Exception as e:
             return jsonify({'success': False, 'error': str(e)})
    else:
        try:
            patients = query_db("SELECT * FROM patients ORDER BY id DESC")
            return jsonify({'patients': patients if patients else []})
        except:
             return jsonify({'patients': []})

@app.route('/api/doctors', methods=['GET'])
def api_doctors():
    try:
        doctors = query_db("SELECT * FROM doctors")
        return jsonify({'doctors': doctors if doctors else []})
    except:
        return jsonify({'doctors': []})

@app.route('/api/appointments', methods=['GET', 'POST'])
def api_appointments():
    if request.method == 'POST':
        data = request.json
        sql = "INSERT INTO appointments (patient_id, doctor_id, appointment_date, symptoms) VALUES (%s, %s, %s, %s)"
        val = (data['patient_id'], data['doctor_id'], data['date'], data['symptoms'])
        try:
             query_db(sql, val)
             return jsonify({'success': True})
        except Exception as e:
             return jsonify({'success': False, 'error': str(e)})
    else:
        try:
            sql = """
                SELECT a.id, p.name as patient_name, d.name as doctor_name, a.appointment_date, a.status 
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                ORDER BY a.appointment_date DESC
            """
            appts = query_db(sql)
            return jsonify({'appointments': appts if appts else []})
        except:
            return jsonify({'appointments': []})

@app.route('/api/billing', methods=['GET', 'POST'])
def api_billing():
    if request.method == 'POST':
        data = request.json
        sql = "INSERT INTO bills (patient_id, amount, status) VALUES (%s, %s, 'Unpaid')"
        val = (data['patient_id'], data['amount'])
        try:
            query_db(sql, val)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        try:
            sql = """
                SELECT b.id, p.name as patient_name, b.amount, b.bill_date, b.status
                FROM bills b
                JOIN patients p ON b.patient_id = p.id
                ORDER BY b.bill_date DESC
            """
            bills = query_db(sql)
            return jsonify({'bills': bills if bills else []})
        except:
            return jsonify({'bills': []})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
