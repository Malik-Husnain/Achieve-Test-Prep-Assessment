# 📘 Smart Book Recommender & Performance Tracker

This is a Django-based backend project that allows authenticated users to track their course progress and receive personalized book recommendations using external APIs like Gutendex and OpenLibrary.

---

## 🚀 Setup Instructions

### 1️⃣ Create a Virtual Environment
To isolate dependencies:

```bash
# Python 3.8+
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

---

### 2️⃣ Install Dependencies
Install required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Configure Environment Variables

Create a `.env` file in the root of the project (if needed):

```
# .env (optional if using hardcoded secrets/session keys)
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

> Make sure you’ve set up Django to read `.env` using `python-decouple`, `os.environ`, or similar (if needed).

---

### 4️⃣ Run Migrations and Start Server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Access the app at: `http://127.0.0.1:8000/`

---

### 5️⃣ Run Unit Tests

Run all tests in the project using:

```bash
python manage.py test
```

This will test APIs such as:
- Course listing
- Adding progress
- Book recommendations
- Session and login flow

---

## 🔗 External APIs Used
- Platzi Fake Store API (JWT Auth)
- Gutendex API (Book content)
- OpenLibrary API (Fallback book data)

---

## 🧪 Features Overview
- JWT-based login
- Session-based course tracking
- External API integration for recommendations
- Pagination for book recommendations
- Add courses directly from recommendations
- Simple HTML+JS frontend included
## 🌐 Navigation & URL Guide

| **URL Path**              | **Purpose**                                  |
|---------------------------|-----------------------------------------------|
| `/login/`                 | User login using JWT                          |
| `/logout/`                | Clears session and logs out                   |
| `/progress/`              | Main dashboard for user progress              |
| `/api/courses/`           | API to list course progress (`GET`)           |
| `/api/recommendations/`   | Fetch paginated book recommendations (`GET`)  |
| `/api/progress/add/`      | Add a course via `POST` request               |

---

## 📂 File Structure Overview
```
├── core/
│   ├── views.py         # All views and API logic
│   ├── models.py        # UserProgress model
│   ├── tests.py         # Unit tests
│   └── templates/       # HTML files
├── static/
│   └── styles.css       # Custom styling
├── requirements.txt
├── .env (optional)
├── manage.py
└── README.md
```

---

## 📬 Questions or Issues?
Open a GitHub issue or submit a pull request. Contributions are welcome!

---

