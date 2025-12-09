# DocterQR
> 🚧 **Project Status:** Work in Progress  
> This project is actively under development. Features, UI, and APIs are subject to change.

# 🩺 Doctor QR – Smart Patient History Collection System

Doctor QR is a web-based healthcare application that helps doctors collect and review patient history efficiently using QR codes.

Each doctor can generate a unique QR code. When patients scan the QR code, they are presented with a customizable medical questionnaire. Their responses are securely stored and displayed in the respective doctor’s dashboard for quick review.

---

## 🚀 Features

### Doctor Side
- Doctor registration & authentication
- Individual doctor dashboard
- Generate unique QR code
- Create & modify patient questionnaire
- View patient list with submitted medical histories
- Quick patient history overview

### Patient Side
- Scan doctor’s QR code
- Answer medical history questions
- Submit responses without login

---

## 🏗️ Tech Stack

### Backend
- **Django**
- Django REST Framework
- SQLite / PostgreSQL
- JWT Authentication

### Frontend
- **Node.js**
- Tailwind CSS
- REST API integration

---

## 🔐 System Workflow

1. Doctor registers and logs in
2. Doctor generates a unique QR code
3. Patient scans QR code
4. Patient answers medical questions
5. Data is saved in backend
6. Doctor reviews patient history in dashboard

---

## 📸 Screenshots

_Add screenshots inside `docs/screenshots/`_

---

## 🛠️ Setup Instructions

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
