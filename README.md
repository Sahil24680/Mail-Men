# 📬 Mail Men

**Mail Men** is a Gmail-style email management web app built with **Django** and **Django REST Framework**, deployed on **AWS EC2**. It supports full email CRUD, user authentication, search, and profile uploads — all in a clean, responsive interface.

---

## 🚀 Features

- 🔐 User authentication (login/register/logout)
- 📧 Send, delete, and reply to emails
- ⭐ Star, archive, and track emails
- 🔍 Search emails by subject, sender, or body
- 🖼️ Upload profile pictures
- ☁️ Deployed on AWS EC2 for global access

---

## 🛠 Tech Stack

| Tool / Tech            | Purpose             |
|------------------------|---------------------|
| Django                 | Backend framework   |
| Django REST Framework  | API layer           |
| SQLite                 | Development database|
| AWS EC2                | Deployment          |
| HTML, CSS              | Frontend UI         |
| Tailwind CSS           | Styling framework   |
| Postman                | API testing         |
| Jest                   | Frontend testing (used in related projects) |

---

## 📁 Folder Structure

Mail-Men/
├── email_api/ # Email models, serializers, views
├── email_sender/ # Custom logic for sending emails
├── login/ # User login & registration
├── media/ # Uploaded profile images
├── static/ # Static files (CSS, etc.)
├── templates/ # HTML templates
├── db.sqlite3 # Local development database
└── manage.py # Django project manager

yaml
Copy
Edit

---

## ⚙️ Getting Started

### Step-by-Step Setup

1. **Clone the Repository**

```bash
git clone https://github.com/Sahil24680/Mail-Men.git
cd Mail-Men
Set Up the Virtual Environment

bash
Copy
Edit
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run Database Migrations

bash
Copy
Edit
python manage.py migrate
Start the Development Server

bash
Copy
Edit
python manage.py runserver
Visit the App in Your Browser

cpp
Copy
Edit
http://127.0.0.1:8000
