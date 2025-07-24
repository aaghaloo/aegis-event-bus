# app/cli.py
import datetime as dt
import os

import typer
from dotenv import load_dotenv
from jose import jwt

from app.utils.time import utcnow

load_dotenv()
app = typer.Typer()

SECRET = os.getenv("SECRET_KEY")
ALG = os.getenv("ALGORITHM", "HS256")


@app.command(help="Generate a short-lived admin JWT")
def create_token(username: str, minutes: int = 60):
    """Generates a JWT for the given username, valid for a number of minutes."""
    exp = utcnow() + dt.timedelta(minutes=minutes)
    token = jwt.encode({"sub": username, "exp": exp}, SECRET, algorithm=ALG)
    typer.echo(f"Generated token for user '{username}':")
    typer.echo(token)


if __name__ == "__main__":
    app()
