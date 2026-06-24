from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy import text

from database import engine

import random
import string

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")


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
            text(
                """
                SELECT *
                FROM urls
                ORDER BY id DESC
                """
            )
        ).fetchall()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
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
        url="/",
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
                WHERE short_code = :code
                """
            ),
            {
                "code": code
            }
        ).fetchone()

    if result:
        return RedirectResponse(url=result[0])

    return {
        "error": "URL not found"
    }