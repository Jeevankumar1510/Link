from fastapi import FastAPI
app = FastAPI()
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import URL

import random
import string



def generate_code():
    return ''.join(
        random.choices(
            string.ascii_letters +
            string.digits,
            k=6
        )
    )

@app.get("/")
def home():
    return {"message":"API Working"}


@app.post("/shorten")
def shorten_url(data: dict):

    db: Session = SessionLocal()

    code = generate_code()

    new_url = URL(
        short_code=code,
        original_url=data["url"]
    )

    db.add(new_url)
    db.commit()

    return {
        "short_url": f"/api/{code}"
    }

@app.get("/{code}")
def redirect_url(code:str):

    db = SessionLocal()

    url = db.query(URL)\
        .filter(URL.short_code==code)\
        .first()

    if not url:
        raise HTTPException(
            status_code=404,
            detail="Not Found"
        )

    return RedirectResponse(
        url.original_url
    )

