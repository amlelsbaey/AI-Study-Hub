# 📚 AI Study Hub

### A Django MVT Web Application with Integrated AI Assistant

AI Study Hub is a web-based study management platform built with **Django** and **PostgreSQL**. It helps students organize their academic life by managing tasks, notes, study resources, and study sessions in one place.

The project also integrates an **AI Assistant** to provide intelligent study support and improve students' productivity.

---

## ✨ Features

### 🔐 Authentication & Account Management

* User Registration
* Login & Logout
* Profile Management
* Update Profile Information
* Change Password
* Email Verification
* Password Reset

### 📊 Dashboard

The dashboard provides an overview of the user's study activity, including:

* Total Tasks
* Total Notes
* Total Resources
* Recent Tasks
* Study Statistics
* Charts and Progress Information

### ✅ Study Planner (Tasks)

Users can manage their study tasks through:

* Add Tasks
* Edit Tasks
* Delete Tasks
* Mark Tasks as Completed
* Due Dates
* Priority Levels
* Task Filtering

### 📝 Notes

Users can create and organize their study notes:

* Create Notes
* View Notes
* Edit Notes
* Delete Notes
* Note Categories
* Search Notes
* Organize Study Content

### 📚 Resources

Users can save useful learning materials:

* Resource Title
* Description
* Resource Type
* External Links
* File Uploads
* Resource Filtering
* Search

### 🤖 AI Assistant

AI Study Hub includes an integrated AI assistant designed to help students study more efficiently.

Depending on the implemented AI services, the assistant can provide features such as:

* 💬 AI Study Chat
* 📄 Summarization
* 🧠 Quiz Generation

The AI integration was implemented independently as part of the project requirements.

### 🎨 Additional Features

* 🌙 Dark Mode
* 🔎 JavaScript Live Search
* 🔍 Server-side Filtering
* 📁 File Uploads
* 🖼️ Profile Image Upload
* 📧 Email Verification
* 🔑 Password Reset
* 📊 Charts
* 📑 PDF Export
* 📱 Responsive Design

---

## 🛠️ Technologies

### Backend

* Python
* Django
* Django MVT Architecture

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* PostgreSQL

### AI

* AI API integration

### Other Tools

* Git
* GitHub

---

## 🏗️ Project Architecture

The project follows the **Django MVT (Model-View-Template)** architecture.

```text
AI Study Hub
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
│
├── study/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
│
├── resources/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── ai_assistant/
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
│
├── templates/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🗄️ Database

AI Study Hub uses **PostgreSQL** as its relational database.

The database is designed using relationships such as:

* One-to-Many
* Many-to-Many
* Foreign Keys

The project contains approximately **8–10 related tables** to manage users, tasks, notes, resources, categories, study sessions, and other application data.

An **ERD (Entity Relationship Diagram)** is included with the project documentation.

---

## 🔎 Search & Filtering

The application provides multiple ways to find study content quickly.

### JavaScript Live Search

Users can search through displayed content instantly without reloading the page.

### Server-Side Search

Django handles database-level searching using queries such as:

* Title
* Description
* Resource Type
* Note Content

### Filtering

Users can filter resources and study content based on categories and types.

---

## 🌙 Dark Mode

AI Study Hub includes a dark mode interface that can be toggled by the user.

The selected theme is stored using **Local Storage**, allowing the user's preference to persist between pages and sessions.

---

## 📊 Dashboard & Charts

The dashboard provides visual information about the user's study activity.

Examples include:

* Task Statistics
* Completed vs. Pending Tasks
* Study Progress
* Recent Activity

Charts are implemented using **Chart.js**.

---

## 📑 PDF Export

Users can export selected study information into PDF format.

PDF export is implemented on the client side using **html2pdf.js**.

---

## 🔒 Security

The project uses Django's built-in security mechanisms, including:

* CSRF Protection
* Authentication System
* Login Required Views
* Password Hashing
* User-specific Data Access
* Django Form Validation

Users can only access and manage their own study data.

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI_Study_Hub
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add the required configuration.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

AI_API_KEY=your-ai-api-key
```

> Do not commit your `.env` file or API keys to GitHub.

### 5. Create the PostgreSQL Database

Create a PostgreSQL database and configure its credentials in the `.env` file.

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

---

## 📦 Requirements

Main technologies and dependencies include:

```text
Python
Django
PostgreSQL
psycopg
Chart.js
html2pdf.js
AI API
```

The complete Python dependencies are available in:

```text
requirements.txt
```

---

## 👥 Team

This project was developed by a team of **2 members** as part of the **Django Web Development** course.

| Member        | Role                               |
| ------------- | ---------------------------------- |
| Amal Mohamed  | Full Stack Developer               |
| Nada Nasser   | Full Stack Developer               |

---

## 🎓 Course Information

**Course:** Django Web Development
**Architecture:** Django MVT
**Database:** PostgreSQL
**Project Type:** Academic Project
**Team Size:** 2 Members
**Submission Date:** August 19, 2026

---

## 📋 Project Requirements

The project was developed using the required technologies:

* HTML
* CSS
* JavaScript
* Python
* Django MVT
* PostgreSQL

The project does **not** use:

* Django REST Framework
* React
* Angular
* Vue
* Flask
* FastAPI
* Firebase

---
