# 🏋️‍♀️ Fitness Tracker API

A RESTful API built with **Django Rest Framework (DRF)** that enables users to track their fitness activities, calculate leaderboards, and manage authentication using JWT.  
Deployed live on **Render** and fully testable via **Postman**.

---

## 🚀 Live Demo

**Base URL:**  
👉 [https://fitness-tracker-alx-capstone-4.onrender.com](https://fitness-tracker-alx-capstone-4.onrender.com)

---

## 📦 Features

- 👤 **User Authentication** — JWT-based login, signup, and token refresh.  
- 🏃 **Activity Management** — Add, view, update, and delete fitness activities.  
- 🏅 **Leaderboard** — Compare users’ performance (daily, weekly, and all-time).  
- ⚙️ **Admin Panel** — Manage users and activities via Django admin.  
- 🌍 **CORS & Whitenoise Support** — Configured for frontend integration and static file hosting.

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Django 4.2, Django Rest Framework |
| **Auth** | Simple JWT |
| **Database** | SQLite (default) |
| **Server** | Gunicorn + Render |
| **Other** | Django-Allauth, CORS Headers, Whitenoise |

---

## 🧩 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|-----------|--------------|----------------|
| `POST` | `/api/auth/register/` | Register new user | ❌ |
| `POST` | `/api/token/` | Get access & refresh tokens | ❌ |
| `POST` | `/api/token/refresh/` | Refresh access token | ❌ |
| `GET` | `/api/activities/` | List all activities | ✅ |
| `POST` | `/api/activities/` | Create a new activity | ✅ |
| `GET` | `/api/activities/<id>/` | Retrieve specific activity | ✅ |
| `PUT` | `/api/activities/<id>/` | Update activity | ✅ |
| `DELETE` | `/api/activities/<id>/` | Delete activity | ✅ |
| `GET` | `/api/activities/leaderboard/?period=weekly` | View leaderboard | ✅ |

---

## 🔐 Authentication

This API uses **JWT (JSON Web Token)** for authentication.

1. Register a new user via `/api/auth/register/`
2. Obtain tokens:
   ```json
   POST /api/token/
   {
     "email": "you@example.com",
     "password": "yourpassword"
   }
