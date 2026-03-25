# Maverick International School Portal

Welcome to the Maverick International School Portal! This project consists of a **Django Backend** and an **HTML/JS Frontend**.

## 🚀 Quick Start Guide (Windows)

To get the entire project running, follow these steps:

### 1. Start the Backend API
Open a new terminal and run:
```powershell
# Navigate to the backend folder
cd backend

# Activate the virtual environment
..\.venv\Scripts\activate

# Run the Django server
python manage.py runserver
```
The API will be available at **http://127.0.0.1:8000**.

### 2. Start the Frontend
Open **another** terminal window and run:
```powershell
# In the root folder (where index.html is)
python -m http.server 5500
```
The Portal UI will be available at **http://127.0.0.1:5500**.

### 3. Accessing the Portal
- **Login**: [http://127.0.0.1:5500/index.html](http://127.0.0.1:5500/index.html)
- **Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (Email: `admin@maverick.edu.ng` / Pass: `admin123`)

---

## 🛠 Key Commands
- **Seed Data**: `python manage.py seed_results` (Run inside `backend` with venv active)
- **Migrations**: `python manage.py migrate`
