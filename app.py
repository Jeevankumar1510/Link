from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from database import engine
import random
import string

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def generate_code():
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=6
        )
    )

@app.get("/")
def home(request: Request):

    with engine.connect() as conn:
        urls = conn.execute(
            text("SELECT * FROM urls")
        ).fetchall()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "urls": urls
        }
    )

@app.post("/shorten")
async def shorten(request: Request):

    form = await request.form()

    original_url = form.get("url")

    short_code = generate_code()

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO urls
                (original_url, short_code)
                VALUES
                (:url, :code)
                """
            ),
            {
                "url": original_url,
                "code": short_code
            }
        )

    return RedirectResponse(
        "/",
        status_code=303
    )

@app.get("/{code}")
def redirect_url(code: str):

    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT original_url
                FROM urls
                WHERE short_code=:code
                """
            ),
            {"code": code}
        ).fetchone()

    if result:
        return RedirectResponse(result[0])

    return {"error": "URL not found"}