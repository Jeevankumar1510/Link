# URL Shortener

## Project Overview

This project is a URL Shortener web application developed using **FastAPI**, **HTML**, **CSS**, **JavaScript**, **Supabase PostgreSQL**, and **Render**.

The application allows users to submit a long URL and generates a unique short URL. The original URL and generated short code are stored in a Supabase PostgreSQL database. When a user visits the generated short URL, the application retrieves the corresponding original URL from the database and automatically redirects the user to it.

The project demonstrates backend API development, database integration, URL routing, and cloud deployment.

---

# Features

* Generate unique short URLs
* Redirect users to the original URL
* Store URLs in a Supabase PostgreSQL database
* Reuse existing short URLs for duplicate links
* Responsive and clean user interface
* Deployed on Render
* Connected to a real cloud database

---

# Technology Stack

### Backend

* FastAPI

### Frontend

* HTML
* CSS
* JavaScript

### Database

* Supabase PostgreSQL

### Deployment

* Render

### Version Control

* Git & GitHub

---

# Project Structure

```text
Link/
│
├── app.py
├── database.py
├── requirements.txt
├── render.yaml
├── .env
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── README.md
```

---

# How to Run the Project Locally

## Step 1: Clone the Repository

Clone the GitHub repository to your local machine.

```bash
git clone https://github.com/Jeevankumar1510/Link.git

cd Link
```

---

## Step 2: Create a Virtual Environment

Create a virtual environment to isolate project dependencies.

```bash
python -m venv venv
```

---

## Step 3: Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## Step 4: Install Dependencies

Install all required Python packages.

```bash
pip install -r requirements.txt
```

---

## Step 5: Configure Environment Variables

Create a file named `.env` in the project root directory.

Add the required environment variable.

```
DATABASE_URL
```

This variable stores the PostgreSQL connection string used to connect the application to the Supabase database.

For security reasons, the actual value should never be committed to GitHub.

---

## Step 6: Run the Application

Start the FastAPI development server.

```bash
uvicorn app:app --reload
```

Open the application in your browser.

```
http://127.0.0.1:8000
```

The application is now running locally.

---

# Environment Variables

The application requires the following environment variable.

| Variable Name | Description                                                                     |
| ------------- | ------------------------------------------------------------------------------- |
| DATABASE_URL  | Connection string used to connect FastAPI with the Supabase PostgreSQL database |

Environment variables are used to keep sensitive information, such as database credentials, separate from the source code. This improves security and allows different configurations for local development and production.

---

# Database Schema

The application uses a PostgreSQL database hosted on Supabase.

Table Name

```
urls
```

| Column       | Type        | Description                                          |
| ------------ | ----------- | ---------------------------------------------------- |
| id           | SERIAL      | Primary key for each record                          |
| original_url | TEXT        | Stores the original URL entered by the user          |
| short_code   | VARCHAR(10) | Stores the generated unique short code               |
| created_at   | TIMESTAMP   | Stores the date and time when the record was created |

SQL Schema

```sql
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

Each record represents one shortened URL. The `short_code` is unique, ensuring that every shortened link maps to only one original URL.

---

# Application Workflow

1. The user opens the application.
2. A long URL is entered into the input field.
3. FastAPI receives the request.
4. The application checks whether the URL already exists in the database.
5. If the URL already exists, the existing short code is returned.
6. Otherwise, a new unique short code is generated.
7. The original URL and generated short code are stored in the Supabase PostgreSQL database.
8. The application displays the generated short URL.
9. When a user clicks the short URL, FastAPI extracts the short code.
10. The application searches the database for the matching original URL.
11. If a matching record is found, the user is redirected to the original website.

---

# Future Improvements

If I had more time, I would enhance the application by adding analytics for shortened URLs.

The analytics feature would include:

* Number of clicks for each short URL
* Date and time of every visit
* Browser and device information
* Geographic location (optional)
* Dashboard to view link statistics

These improvements would make the application more useful by allowing users to monitor how their shortened links are being used.

---

# Why I Chose a Different Stack

The recommended stack for this assignment was **Next.js (Frontend + API Routes)** with **Vercel** for deployment and **Supabase PostgreSQL** as the database.

I chose **FastAPI**, **HTML**, **CSS**, **JavaScript**, **Render**, and **Supabase PostgreSQL** because I wanted to demonstrate backend development using Python. FastAPI is lightweight, high-performance, and well suited for building REST APIs. Since I have experience working with Python, this stack allowed me to develop the application efficiently while meeting all the functional requirements of the assignment. Render provides a simple deployment platform for FastAPI applications, while Supabase offers a reliable managed PostgreSQL database.

---

# Live Application

The project is deployed on Render and is publicly accessible.

https://link-24k5.onrender.com

---

# GitHub Repository

Complete source code, commit history, and project documentation are available on GitHub.

https://github.com/Jeevankumar1510/Link

---

# Author

**Jeevan Kumar**
