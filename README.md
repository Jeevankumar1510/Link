URL SHORTENER - COMPLETE PROJECT EXPLANATION

Project Overview

This is a URL shortening application. Think of it like a service that converts long URLs into shorter, easy to share links. For example, a long URL like https://www.example.com/very/long/page/with/many/parameters becomes something simple like http://localhost:8000/abc123.

The application has three main parts:
1. Frontend - The web page where users enter long URLs
2. Backend - The logic that creates short links and manages redirects
3. Database - Stores the mapping between long URLs and short links

Why This Project Matters

When you have a very long URL, it is hard to share in messages, emails, or social media. This tool solves that problem by generating a short code that redirects to the original URL. This is exactly how services like bit.ly, tinyurl, and short.link work.


COMPLETE FILE BY FILE EXPLANATION

File 1: app.py - The Main Application Logic

This file contains all the backend logic. Here is every line explained:

Line 1: from fastapi import FastAPI, Request
This imports FastAPI, which is the web framework. FastAPI helps create web applications easily. Request is used to get data from the browser.

Line 2: from fastapi.responses import RedirectResponse
This imports RedirectResponse, which redirects users from one URL to another. When someone clicks a short link, this redirects them to the original URL.

Line 3: from fastapi.templating import Jinja2Templates
This imports Jinja2Templates, which is used to display HTML pages with dynamic content. Dynamic means the content changes based on data from the database.

Line 4: from fastapi.staticfiles import StaticFiles
This imports StaticFiles, which serves static files like CSS and JavaScript. Static files do not change based on user input.

Line 5: from sqlalchemy import text
This imports text from SQLAlchemy. SQLAlchemy is used to communicate with the database. Text allows us to write raw SQL queries.

Line 6: from database import engine
This imports the database engine from database.py. The engine is the connection to Supabase database.

Line 7-8: import random, string
These imports provide functions to generate random characters and work with strings.

Line 10: app = FastAPI()
This creates the main FastAPI application. All routes and endpoints are added to this app.

Line 11: app.mount("/static", StaticFiles(directory="static"), name="static")
This serves files from the static folder. When browser requests /static/style.css, it returns the file from static/style.css. This line appears twice in the code.

Line 14: templates = Jinja2Templates(directory="templates")
This tells the application where to find HTML templates. When rendering a page, FastAPI looks in the templates folder.

Line 18-27: def generate_short_link():
This function creates a random 6-character short link. Let me explain line by line:

Line 22-26 creates a random string by selecting 6 random characters from ascii_letters (a-z, A-Z) and digits (0-9). The k=6 means select 6 characters. The ''.join() combines them into one string.

Example output: abc123, XyZ456, aBc789

Line 30-45: @app.get("/")
This defines the home page route. When user visits http://localhost:8000, this function runs.

Line 31: def home(request: Request):
request contains information about the HTTP request from the browser.

Line 33-42: with engine.connect() as conn:
This opens a connection to the database.

Line 34-41: conn.execute(text(...))
This executes a SQL query. The query is:

SELECT * FROM urls ORDER BY id DESC

This selects all data from urls table and orders it by id in descending order. DESC means newest first. This gets all shortened URLs that have been created.

Line 42: .fetchall()
This fetches all results from the query and stores them in urls variable.

Line 44-48: return templates.TemplateResponse(...)
This returns an HTML page. TemplateResponse renders the index.html file and passes data to it.

request=request - The request object needed by Jinja2
name="index.html" - The HTML file to render
context={"urls": urls} - Data passed to the HTML template. The template can access urls and display all shortened links.

Line 51-75: @app.post("/shorten")
This route handles when user clicks the Shorten button.

Line 52: async def shorten(request: Request):
Async means this function runs asynchronously. This allows the server to handle multiple requests at the same time without blocking.

Line 54: form = await request.form()
This gets the form data from the HTML form. await waits for the data to arrive.

Line 56: original_url = form.get("url")
This gets the url field from the form. If user types https://example.com, this extracts it.

Line 58: short_link = generate_short_link()
This calls the generate_short_link function to create a random 6-character short link.

Line 60-67: with engine.begin() as conn:
This opens a database connection for writing data.

Line 61-66: conn.execute(text(...))
This executes an INSERT query:

INSERT INTO urls (original_url, short_link) VALUES (:url, :link)

This adds a new row to the urls table with the original URL and the short link.

:url and :link are placeholders that prevent SQL injection attacks.

The actual values are provided in the dictionary:
{"url": original_url, "link": short_link}

Line 69-71: return RedirectResponse(...)
After saving to database, this redirects the user back to the home page (/). Status code 303 means "See Other", which is correct for POST to GET redirect.

Line 74-104: @app.get("/{code}")
This route handles when someone visits a short link like /abc123

Line 75: def redirect_url(code: str):
code is extracted from the URL. If someone visits /abc123, code becomes "abc123".

Line 77-86: with engine.connect() as conn:
Opens database connection.

Line 78-84: conn.execute(text(...))
This executes a SELECT query:

SELECT original_url FROM urls WHERE short_link = :link

This searches the urls table for a row where short_link matches the link variable.

Line 85: .fetchone()
Gets one result from the query. If code exists, result contains the original_url. If not, result is None.

Line 87-88: if result:
If code was found in database:

Line 88: return RedirectResponse(url=result[0])
Redirects to the original URL. result[0] means first column of the result, which is original_url.

Line 90-91: return {"error": "URL not found"}
If code was not found, returns an error message.


File 2: database.py - Database Configuration

This file handles the connection to Supabase.

Line 1: from sqlalchemy import create_engine
Imports create_engine, which creates a database connection.

Line 2: from sqlalchemy.orm import sessionmaker
Imports sessionmaker for creating database sessions. Not used in this project yet.

Line 3: from dotenv import load_dotenv
Imports load_dotenv, which reads the .env file.

Line 4: import os
Imports os, which accesses environment variables and file system.

Line 6: load_dotenv()
This loads all variables from .env file into environment.

Line 8: DATABASE_URL = os.getenv("DATABASE_URL")
Gets the DATABASE_URL from environment. This is the connection string to Supabase database.

Line 10: engine = create_engine(DATABASE_URL)
Creates the database engine using the connection string. This engine is imported in app.py and used to connect to database.

Line 12-15: SessionLocal = sessionmaker(...)
Creates a session factory for creating database sessions. This is prepared for future use.


File 3: requirements.txt - Dependencies

This file lists all Python packages needed.

fastapi - The web framework
uvicorn - The server that runs FastAPI
sqlalchemy - The tool to communicate with database
psycopg2-binary - The driver that allows Python to connect to PostgreSQL
python-dotenv - Reads .env file
jinja2 - Template engine for rendering HTML
python-multipart - Parses form data


File 4: render.yaml - Deployment Configuration

This file tells Render how to deploy the application.

It specifies:
- Web service type
- Service name
- Python environment
- Build command (pip install -r requirements.txt)
- Start command (uvicorn app:app ...)


File 5: templates/index.html - The Web Page

This is the HTML that users see. Key parts:

Line 25: form action="/shorten" method="post"
This creates a form that sends data to /shorten endpoint when submitted.

Line 27: input type="url" name="url"
This is the text box where users paste their long URL. name="url" means the value is sent as url parameter.

Line 28: button type="submit"
This is the Shorten button that submits the form.

Line 47: {% for url in urls %}
This is Jinja2 templating. It loops through all urls from the context and displays each one.

Line 50: a class="link-short" href="/{{ url.short_link }}"
This creates a clickable link for each short link. {{ url.short_link }} inserts the actual short link value.

Line 51: p class="link-original"
This displays the original long URL next to the short code.


File 6: static/style.css - Styling

This file contains CSS that makes the page look nice with colors, fonts, and layout.


STEP BY STEP FLOW OF THE APPLICATION

Flow 1: User Visits Home Page

Step 1: User opens browser and types http://localhost:8000
Step 2: Browser sends GET request to server
Step 3: FastAPI routes this to @app.get("/") function in app.py
Step 4: Function opens database connection
Step 5: Function executes SELECT query to get all urls from database ordered by newest first
Step 6: Function receives list of all shortened URLs
Step 7: Function renders index.html template and passes the urls list
Step 8: Jinja2 generates HTML by looping through urls and creating link cards
Step 9: HTML is sent back to browser
Step 10: User sees web page with form to enter URL and list of previously created short links


Flow 2: User Creates Short Link

Step 1: User types a long URL like https://www.example.com/very/long/page
Step 2: User clicks Shorten button
Step 3: Browser submits form as POST request to /shorten endpoint
Step 4: Form data is captured by FastAPI
Step 5: @app.post("/shorten") function runs
Step 6: Function extracts the URL from form using form.get("url")
Step 7: Function calls generate_short_link() which creates random 6-character link like "abc123"
Step 8: Function opens database connection
Step 9: Function executes INSERT query to save original_url and short_link to urls table
Step 10: Database creates new row with id, original_url, short_link, and created_at
Step 11: Function returns RedirectResponse to home page
Step 12: Browser redirects to http://localhost:8000
Step 13: Home page now shows the new shortened link in the list
Step 14: User can copy the short link and share it


Flow 3: User Clicks Short Link

Step 1: Someone receives the short link like http://localhost:8000/abc123
Step 2: They click it or paste it in browser
Step 3: Browser sends GET request with /abc123
Step 4: FastAPI routes to @app.get("/{code}") function
Step 5: code parameter is set to "abc123"
Step 6: Function opens database connection
Step 7: Function executes SELECT query to find row where short_link = "abc123"
Step 8: Database returns the original_url from that row
Step 9: Function returns RedirectResponse to the original URL
Step 10: Browser automatically redirects and opens the original long URL
Step 11: User arrives at the destination website


DATABASE SCHEMA COMPLETE EXPLANATION

Table Name: urls

This table has 4 columns. Here is what each does:

Column 1: id
Data Type: SERIAL
SERIAL means automatically incrementing number starting from 1, 2, 3, etc.
Constraint: PRIMARY KEY means each id is unique and no two rows can have same id
Purpose: This is the unique identifier for each row. Every shortened link gets one id.

Column 2: original_url
Data Type: TEXT
TEXT is a data type that stores string of text of any length
Constraint: NOT NULL means this field must always have a value. Cannot be empty.
Purpose: This stores the long URL that the user wants to shorten
Example: https://www.github.com/user/repository

Column 3: short_link
Data Type: VARCHAR(6)
VARCHAR(6) means variable character string of maximum 6 characters
Constraint: UNIQUE means no two rows can have same short_link. Each link is different.
Constraint: NOT NULL means short_link must always have a value
Purpose: This stores the 6-character random link that creates the short URL
Example: abc123

Column 4: created_at
Data Type: TIMESTAMP
TIMESTAMP stores date and time
Constraint: DEFAULT CURRENT_TIMESTAMP means if not provided, automatically use current date and time
Purpose: Records when the URL was added
Example: 2024-01-15 10:30:45

Sample Data in Table:

id | original_url | short_link | created_at
1 | https://github.com/user | abc123 | 2024-01-15 10:30:45
2 | https://www.example.com | xyz789 | 2024-01-15 10:35:22
3 | https://stackoverflow.com | def456 | 2024-01-15 10:40:10

When you visit /abc123, the app searches for short_link = "abc123", finds id 1, retrieves https://github.com/user, and redirects there.


KEY CONCEPTS AND TERMS TO UNDERSTAND FOR INTERVIEW

HTTP Request Methods

GET - Used to retrieve data from server. When you type URL in browser, it is a GET request.
POST - Used to send data to server. When form is submitted, it is usually a POST request.
Both are used in this project.

Async and Await

async def shorten() - The async keyword means this function can run without blocking other requests.
await request.form() - The await keyword means wait for the form data to arrive before proceeding.
This is important because while waiting for form data, the server can handle other requests from other users.

Database Transactions

with engine.begin() as conn: - The begin() creates a transaction. If something goes wrong, the entire transaction is rolled back (undone). This ensures data consistency.

with engine.connect() as conn: - The connect() just opens a connection without transaction protection. Used for reading data.

SQL Injection Prevention

:url and :link are placeholders in SQL queries. Instead of putting the user input directly in the query like:

INSERT INTO urls (original_url, short_link) VALUES ('user_input', 'link')

We use placeholders:

INSERT INTO urls (original_url, short_link) VALUES (:url, :link)

Then pass values separately. This prevents SQL injection attacks where malicious code could be injected.

Jinja2 Templating

{% for url in urls %} - Loop through all urls
{{ url.short_link }} - Print the value of short_link
{% else %} - If urls is empty
{% endfor %} - End the loop

This allows HTML to be dynamic based on database data.

Redirects

When user creates a short link, they are redirected to home page using status code 303.
When user clicks a short link, they are redirected to original URL using status code 307.
Different codes have different meanings in HTTP protocol.


INTERVIEW QUESTIONS YOU WILL BE ASKED AND HOW TO ANSWER

Question 1: What does this project do?

Answer: This project is a URL shortener. It allows users to convert long URLs into short, easy-to-share links. For example, a long URL like https://www.github.com/user/repository/issues/123/comments becomes something like /abc123. When someone clicks the short link, it redirects them to the original long URL.

Question 2: Explain the architecture

Answer: The project has three parts. First is the frontend which is the HTML form where users enter URLs. Second is the backend which is FastAPI application that handles requests, generates short links, and communicates with database. Third is the database which stores the mapping between long URLs and short links. User -> FastAPI -> Database.

Question 3: What happens when user visits home page?

Answer: When user visits home page, FastAPI executes the @app.get("/") function. This function connects to the database and executes a SELECT query to retrieve all URLs from the urls table ordered by newest first. Then it renders the index.html template and passes the list of URLs. Jinja2 loops through the URLs and generates HTML with cards showing each short link and original URL. This HTML is sent to browser.

Question 4: What happens when user enters a URL and clicks Shorten?

Answer: The browser submits a POST request to the /shorten endpoint. FastAPI receives the form data and calls the generate_short_link function which creates a random 6-character link using letters and numbers. Then it opens a database connection and executes an INSERT query to save both the original URL and the short link to the urls table. After saving, it redirects user back to home page where they can see the new link.

Question 5: What happens when someone clicks a short link?

Answer: When someone visits a short link like /abc123, FastAPI routes this to the @app.get("/{link}") function where link becomes "abc123". The function connects to database and executes a SELECT query searching for the row where short_link equals "abc123". If found, it retrieves the original_url from that row and returns a RedirectResponse which tells browser to redirect to the original URL. If not found, it returns error message.

Question 6: Why did you use FastAPI?

Answer: I used FastAPI because it is very fast and modern. It can handle many requests quickly and efficiently. FastAPI has built-in support for async/await which allows the server to handle multiple requests at the same time without blocking. It also has automatic interactive API documentation called Swagger which makes testing easy. The code is clean and easy to understand.

Question 7: Why did you use Supabase?

Answer: I used Supabase because it provides a managed PostgreSQL database which means I do not need to install or maintain any database software on my computer. The free tier is generous and includes automatic backups so data is safe. Supabase provides the database connection string which I just need to add to environment variables.

Question 8: Why did you use Render?

Answer: I used Render because it connects directly to GitHub and automatically deploys code whenever I push updates. It provides a free tier for testing and learning. Render handles server management and scaling automatically, so I can focus on code instead of managing servers. The deployment process is very simple and fast.

Question 9: What is the purpose of the environment variable?

Answer: The DATABASE_URL is an environment variable that contains the PostgreSQL connection string to Supabase. This includes username, password, host, port, and database name. I use environment variables instead of hardcoding the connection string because it is more secure. Sensitive information is not included in the code that is pushed to GitHub. On local machine, it is in .env file. On production server like Render, it is set in the dashboard.

Question 10: How does the generate_code function work?

Answer: The generate_short_link function creates a random 6-character link. It uses string.ascii_letters which contains all lowercase and uppercase letters (a-z, A-Z), and string.digits which contains all numbers (0-9). Then it uses random.choices to select 6 random characters from this combined pool. Finally, ''.join() combines them into one string. For example, it might generate "aBc123" or "XyZ456". This gives extremely low probability of collision since there are about 2 billion possible combinations.

Question 11: What is async/await and why is it used?

Answer: async/await is Python syntax for asynchronous programming. The async keyword on a function allows it to be non-blocking. The await keyword pauses execution until a result is received, but allows other requests to be processed meanwhile. In the shorten function, we use await request.form() to wait for form data. While this request waits for data, the server can process requests from other users. This makes the application much more efficient, especially under high load.

Question 12: Explain the database schema

Answer: The database has one table called urls with 4 columns. The id column is auto-incrementing primary key that identifies each row. The original_url column stores the long URL that user provided. The short_link column stores the randomly generated 6-character link. The created_at column automatically records the timestamp when the row was added. For example, if I shorten https://github.com/user to abc123, a row is created with id=1, original_url=https://github.com/user, short_link=abc123, created_at=current time.

Question 13: How do you prevent SQL injection?

Answer: I prevent SQL injection by using parameterized queries with placeholders. Instead of putting user input directly in the SQL query, I use :url and :link as placeholders. Then I pass the actual values separately in a dictionary. For example, instead of INSERT INTO urls VALUES ('user_input_here', 'link_here'), I write INSERT INTO urls VALUES (:url, :link) and pass {url: user_input, link: link_here}. This way the database driver handles the values safely and prevents any malicious SQL code from being executed.

Question 14: What files are in this project and what do they do?

Answer: app.py contains all the backend logic with three endpoints. database.py handles the database connection by reading DATABASE_URL from environment and creating the engine. requirements.txt lists all Python packages needed. render.yaml contains deployment configuration for Render. templates/index.html is the HTML form and display page that users interact with. static/style.css contains styling for the web page.

Question 15: How would you improve this project?

Answer: The best improvement would be to add click tracking. Right now there is no way to see how many times each short link was clicked or when it was last accessed. To implement this, I would add two columns to the urls table: click_count and last_accessed. Then in the redirect endpoint, I would increment click_count and update last_accessed timestamp every time someone clicks a short link. This would provide valuable analytics and help users understand which links are most popular.


PRACTICAL: HOW TO RUN THE PROJECT LOCALLY STEP BY STEP

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
    short_link VARCHAR(6) UNIQUE NOT NULL,
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

Column 3: short_link
Data Type: VARCHAR(6)
Constraints: UNIQUE, NOT NULL
Purpose: Stores the randomly generated 6 character link used to create the short URL, each link must be unique and must have a value

Column 4: created_at
Data Type: TIMESTAMP
Constraints: DEFAULT CURRENT_TIMESTAMP
Purpose: Automatically records the exact date and time when the URL was added to the database

Sample Data:

id | original_url | short_link | created_at
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

Step 2: The application generates a random 6 character link using letters and numbers

Step 3: The application saves both the original URL and the short link to the database

Step 4: The application shows the user the new short link

Step 5: When someone clicks or visits the short link, the application looks up the short link in the database

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
