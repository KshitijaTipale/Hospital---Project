# Hospital Management System - Interview Preparation Guide

## 1. Project Overview
**One-Liner:** "I built a full-stack Hospital Management System using **Flask (Python)** and **MySQL** to manage hospital operations efficiently."

**Key Features:**
- **Admin Dashboard:** Overview of doctor availability, patient count, and appointments.
- **Patient Management:** CRUD operations for patient records.
- **Appointment System:** Scheduling appointments between patients and doctors.
- **Access Control:** Secure login for administrators.
- **Responsive UI:** Custom CSS designed for a professional look.

## 2. Technical Stack & Logic
### **Backend: Flask (Python)**
- **Why Flask?** "I chose Flask because it's lightweight, flexible, and allows me to understand the backend logic (routing, request handling) without too much 'magic' like in Django."
- **Key Logic:**
  - `app.py`: Handles HTTP requests (GET/POST).
  - **API Design:** Used RESTful principles where frontend asks for data via `fetch()` and backend responds with JSON.
  - **Database Connection:** Used `mysql-connector` to execute raw SQL queries for better control and learning purposes (instead of an ORM like SQLAlchemy).

### **Frontend: HTML/CSS/JS**
- **Why No React?** "I wanted to master the fundamentals of DOM manipulation and AJAX/Fetch API before moving to frameworks. This demonstrates I understand how the web works under the hood."
- **Dynamic Content:** Used JavaScript `fetch()` to call my Flask APIs and update the page without reloading (Single Page Application feel).

### **Database: MySQL**
- **Schema Design:**
  - `users`: For authentication.
  - `patients`: Stores personal and medical info.
  - `doctors`: Doctor profiles.
  - `appointments`: Links Patients and Doctors (Many-to-Many relationship).
  - `bills`: Financial records linked to patients.

## 3. Common Interview Questions
**Q: How did you handle database connections?**
A: "I created a helper function `get_db_connection()` that opens a connection for each request and closes it immediately after use to prevent connection leaks. I also used a `try-finally` block to ensure closure even if errors occur."

**Q: How is the login secured?**
A: "For this project, I implemented a session-based login using Flask's `session` object. In a production environment, I would hash passwords using `bcrypt` instead of storing plain text."

**Q: Explain the relationship between Patients and Appointments.**
A: "It's a **One-to-Many** relationship. One Patient can have multiple Appointments, but one specific Appointment belongs to only one Patient. In the database, the `appointments` table has a Foreign Key `patient_id` referencing the `patients` table."

**Q: What was the most challenging part?**
A: *(Pick one)*
- " Designing the database schema to ensure data integrity (Foreign Keys)."
- " implementing the AJAX logic to update tables dynamically without page reloads."

## 4. Run Instructions
1. **Setup Database:** Ensure MySQL is running and `db_config.py` has correct credentials. Run `python init_db.py`.
2. **Start Server:** Run `python app.py`.
3. **Access:** Go to `http://localhost:5000`.
4. **Login:** Use username `admin` and password `admin123`.
