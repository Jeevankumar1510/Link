URL Shortener

A simple application that converts long URLs into short links. Built using FastAPI for the backend, Supabase for the database, and deployed on Render.


How to Run the Project Locally Step by Step

Step 1: Set Up Your Computer
Download and extract the project folder. Open a command prompt or terminal and navigate to the project directory.

Step 2: Create Virtual Environment
Run this command to create an isolated space for this project:

python -m venv venv

Activate the virtual environment:

venv\Scripts\activate

On Mac or Linux, use:
source venv/bin/activate

Step 3: Install Dependencies
Install all required packages by running:

pip install -r requirements.txt

This command reads the requirements.txt file and installs every package listed in it.

Step 4: Set Up Environment Variables
Create a new file named .env in your project root folder. Add the following line to it:

DATABASE_URL=

Do not commit this .env file to version control. Add .env to your .gitignore file.

Step 5: Create Database Table
Log into your Supabase account and go to the SQL Editor. Create a new query and paste this code:

CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(6) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Execute the query to create the table.

Step 6: Start the Application
Run this command to start the application in development mode:

uvicorn app:app --reload

You should see output showing the application is running on http://127.0.0.1:8000

Step 7: Open in Web Browser
Open your web browser and go to http://localhost:8000 to see the application.

To stop the application, press Ctrl+C in the terminal.


Environment Variables Needed

DATABASE_URL

This is the only environment variable required for the application to work. It contains the PostgreSQL connection string from Supabase. The format includes user credentials, host, port, and database name.

For local development, add it to the .env file in the root directory.

For production on Render, add it through the Render dashboard in the Environment section.


Database Table Schema

The application uses one table called urls with the following structure:

Table Name: urls

Column 1: id
Data Type: SERIAL
Constraints: PRIMARY KEY
Purpose: Automatically increments for each new record, provides unique identifier for each URL entry

Column 2: original_url
Data Type: TEXT
Constraints: NOT NULL
Purpose: Stores the full URL that the user wants to shorten, must always have a value

Column 3: short_code
Data Type: VARCHAR(6)
Constraints: UNIQUE, NOT NULL
Purpose: Stores the randomly generated 6 character code used to create the short link, each code must be unique and must have a value

Column 4: created_at
Data Type: TIMESTAMP
Constraints: DEFAULT CURRENT_TIMESTAMP
Purpose: Automatically records the exact date and time when the URL was added to the database

Sample Data:

id | original_url | short_code | created_at
1 | https://www.github.com/user/repository | abc123 | 2024-01-15 10:30:45
2 | https://www.example.com/very/long/page | xyz789 | 2024-01-15 10:35:22
3 | https://stackoverflow.com/questions/12345 | def456 | 2024-01-15 10:40:10


One Thing to Improve or Fix

If given more time, the best improvement would be to add click tracking functionality.

Currently the application has no way to know how many times a shortened link was used or when it was last used. This limits the value of the tool because users cannot see which links are most popular or get any analytics about link usage.

To fix this, add two new columns to the urls table:

click_count - An integer that counts the number of times the short link was clicked

last_accessed - A timestamp that records the most recent date and time the link was accessed

Then modify the redirect endpoint in app.py to increment click_count and update last_accessed each time a user clicks a short link.

This improvement would provide valuable analytics and help users understand which links drive the most traffic or engagement.


Why This Stack Was Chosen

FastAPI

FastAPI was chosen as the backend framework because it is fast and modern compared to older Python web frameworks. It can handle many requests quickly and has built-in automatic documentation for testing the API. FastAPI uses async programming which makes it efficient for applications that handle many users at the same time. It also has simple syntax that makes the code easy to understand and maintain.

Supabase

Supabase was chosen for the database because it is free to start and easy to use. You do not need to install or maintain anything on your computer because Supabase is a hosted PostgreSQL service. The free tier includes automatic backups so your data is safe. Supabase also provides additional features like authentication if needed in the future.

Render

Render was chosen for hosting and deployment because it connects directly to GitHub and automatically deploys new code when you push updates. It provides a free tier for testing and learning. Render handles server management and scaling automatically, so you can focus on your code instead of managing servers.


How the Application Works

When a user submits a long URL through the web form and clicks the Shorten button, the application performs these steps:

Step 1: The application receives the long URL from the form submission

Step 2: The application generates a random 6 character code using letters and numbers

Step 3: The application saves both the original URL and the short code to the database

Step 4: The application shows the user the new short link

Step 5: When someone clicks or visits the short link, the application looks up the short code in the database

Step 6: The application retrieves the original URL and redirects the user to it automatically


Project Files Overview

app.py
Contains the main application code with all the endpoints. Includes the GET route that shows all shortened URLs, the POST route that creates new short links, and the GET route that redirects from short code to original URL.

database.py
Handles the connection to Supabase. This file reads the DATABASE_URL from the environment and creates the database engine that the application uses.

requirements.txt
Lists all Python packages that need to be installed. When you run pip install -r requirements.txt, all packages in this file are installed.

render.yaml
Contains the configuration for deploying the application on Render. Specifies the build command and start command.

templates/index.html
The HTML template that creates the web page users see. Uses Jinja2 templating to display dynamic data.

static/style.css
The CSS file that styles the web page with colors, fonts, and layout.


Deploying to Production

To make the application live on the internet:

Step 1: Push your code to GitHub
Commit all changes and push to your GitHub repository. Make sure .env is in .gitignore so sensitive data is not pushed.

Step 2: Go to Render
Visit https://dashboard.render.com and create a new Web Service.

Step 3: Connect GitHub Repository
Select your GitHub repository and authorize Render to access it.

Step 4: Configure Service Settings
Fill in the following:

Service Name: url-shortener
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app:app --host 0.0.0.0 --port 8000

Step 5: Add Environment Variables
In the Render dashboard, add an environment variable:

Name: DATABASE_URL
Value: Your Supabase connection string

Step 6: Deploy
Click Create Web Service to start the deployment. The application will be built and deployed automatically. This usually takes 2 to 5 minutes.

Step 7: Access Your Live Application
Once deployment is complete, Render provides a public URL where your application is live and accessible to anyone on the internet.


Technologies Used

FastAPI - Web framework for creating the application
Supabase - PostgreSQL database service
Uvicorn - ASGI server for running the application
SQLAlchemy - Tool for communicating with the database
Psycopg2 - PostgreSQL driver for Python
Jinja2 - Template engine for creating HTML pages
Python-dotenv - Loads environment variables from .env file
