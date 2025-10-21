# 🏋️ Fitness Tracker API

A comprehensive **RESTful API** for fitness activity tracking built with **Django** and **Django REST Framework**.  
This API allows users to log, manage, and analyze their fitness activities with robust authentication and analytics features.

---

## 🚀 Features

### **Core Features**
- **User Authentication** – Register and login using username or email  
- **Activity Management** – Full CRUD operations for fitness activities  
- **Activity History** – Filter and view activity history by date range and type  
- **Metrics & Analytics** – Track totals and trends for duration, distance, and calories  
- **Pagination & Sorting** – Efficiently handle large sets of activity data  

### **Advanced Features**
- **Goal Setting** – Define and track personal fitness goals  
- **Workout Plans** – Create structured workout routines  
- **Leaderboards** – Compete with other users  
- **User Profiles** – Access detailed fitness statistics  

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | Django 4.2+, Django REST Framework |
| **Database** | Django ORM with SQLite |
| **Authentication** | JWT Tokens |
| **API Docs** | Auto-generated with DRF |
| **Deployment Ready** | Render / PythonAnywhere / Localhost |

---

## 📋 API Endpoints

### **Authentication Endpoints**
| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login (username/email) |
| POST | `/api/auth/logout/` | User logout |
| GET | `/api/auth/user/` | Get current user info |

---

### **Activity Management**
| Method | Endpoint | Description |
|--------|-----------|-------------|
| GET | `/api/activities/` | List user's activities |
| POST | `/api/activities/` | Create new activity |
| GET | `/api/activities/{id}/` | Get specific activity |
| PUT | `/api/activities/{id}/` | Update activity |
| DELETE | `/api/activities/{id}/` | Delete activity |

---

### **Activity History & Analytics**
| Method | Endpoint | Parameters | Description |
|--------|-----------|-------------|-------------|
| GET | `/api/activities/history/` | `start_date`, `end_date`, `activity_type` | Filtered activity history |
| GET | `/api/activities/metrics/` | `period=week|month|year|all` | Summary metrics |
| GET | `/api/activities/trends/` | `trend_type=weekly|monthly` | Trends over time |
| GET | `/api/activities/recent/` | `limit=10` | Recent activities |

---

### **Goals & Workouts**
| Method | Endpoint | Description |
|--------|-----------|-------------|
| GET/POST | `/api/activities/goals/` | List/Create fitness goals |
| GET/PUT/DELETE | `/api/activities/goals/{id}/` | Manage specific goal |
| GET/POST | `/api/workouts/` | List/Create workout plans |
| GET/PUT/DELETE | `/api/workouts/{id}/` | Manage workout plan |

---

### **Social Features**
| Method | Endpoint | Parameters | Description |
|--------|-----------|-------------|-------------|
| GET | `/api/activities/leaderboard/` | `period=daily|weekly|monthly` | Community leaderboard |
| GET | `/api/activities/leaderboard/my-ranking/` | `period=daily|weekly|monthly` | User's ranking |

---

### **User Profile**
| Method | Endpoint | Parameters | Description |
|--------|-----------|-------------|-------------|
| GET | `/api/activities/profile/` | - | Get user profile with stats |
| GET | `/api/activities/profile/` | `refresh=true` | Refresh profile statistics |

---

## 🗄️ Data Models

### **User Model**
- `username` – Unique username  
- `email` – Unique email address  
- `password` – Hashed password  
- `date_joined` – Account creation date  

### **Activity Model**
- `user` – ForeignKey to User  
- `activity_type` – Running, Cycling, Weightlifting, Swimming, Yoga, etc.  
- `duration` – Duration in minutes (required)  
- `distance` – Distance in kilometers (optional)  
- `calories_burned` – Calories burned (optional)  
- `date` – Activity date (required)  
- `notes` – Additional notes (optional)  

### **Goal Model**
- `user` – ForeignKey to User  
- `goal_type` – distance, duration, calories, activities_count  
- `target_value` – Target value to achieve  
- `deadline` – Goal deadline date  
- `is_completed` – Completion status  

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8+
- Virtualenv

### **Local Development Setup**

```bash
# Clone the repository
git clone https://github.com/yourusername/fitness-tracker-api.git
cd fitness-tracker-api

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your secret key

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
🌍 Live Demo

If deployed, you can view it here:
👉 https://fitness-tracker-alx-capstone-4.onrender.com/
