# Qatar Foundation Admin Portal - Backend Implementation

This repository contains the complete backend implementation for the Qatar Foundation Admin Portal, built during the Certify Me Backend Development Assignment.

## 🚀 Features Implemented

### 1. Authentication System (US-1)
- **Admin Sign Up:** Secure registration with password hashing using `scrypt`.
- **Admin Login:** Session-based authentication with "Remember Me" functionality.
- **Password Reset:** API endpoint for password recovery simulation.
- **Security:** All routes except login/signup are protected and require a valid session.

### 2. Opportunity Management (US-2)
- **View All:** Fetches and displays only the opportunities created by the logged-in admin.
- **Add New:** Full form integration to add new programs/certifications to the database.
- **Delete:** Ability to remove existing opportunities with instant UI updates.
- **Data Persistence:** Replaced all hardcoded mock data with a real SQLite database.

### 3. Frontend Integration
- Patched the provided admin.js to communicate with the Flask API using the fetch API.
- Implemented dynamic loading to clear demo cards and show real database content upon login.
- Served the application via Flask render_template and send_from_directory for a unified full-stack experience.

## 🛠️ Technology Stack
- **Backend:** Python 3.x, Flask
- **Database:** SQLAlchemy (SQLite)
- **Security:** Flask-Login, Werkzeug Security
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)

## 📋 How to Run

1. **Navigate to the project folder:**
powershell
   cd qatar_foundation_admin


2. **Initialize the Virtual Environment:**
   powershell
   python -m venv venv
   .\venv\Scripts\activate
   

3. **Install Dependencies:**
  powershell
   pip install -r requirements.txt
 

4. **Run the Application:**
   powershell
   python app.py
   
   *The application will automatically open in your default browser at http://127.0.0.1:8000.*

---
*Developed as part of the Certify Me Internship Assignment.*
