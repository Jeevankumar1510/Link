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
        result = conn.execute(
            text("""
                SELECT *
                FROM urls
                ORDER BY id DESC
            """)
        )

        urls = []

        for row in result.mappings():

            row = dict(row)

            row["short_url"] = f"{request.base_url}{row['short_code']}"

            urls.append(row)

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

    with engine.begin() as conn:

        existing = conn.execute(
            text("""
                SELECT short_code
                FROM urls
                WHERE original_url = :url
            """),
            {
                "url": original_url
            }
        ).fetchone()

        if existing:

            short_code = existing[0]

        else:

            short_code = generate_code()

            conn.execute(
                text("""
                    INSERT INTO urls
                    (original_url, short_code)
                    VALUES
                    (:url, :code)
                """),
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
            text("""
                SELECT original_url
                FROM urls
                WHERE short_code = :code
            """),
            {
                "code": code
            }
        ).fetchone()

    if result:

        return RedirectResponse(
            url=result[0],
            status_code=307
        )

    return {
        "error": "URL not found"
    }