from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import status
import run
import asyncio
import os

api_keys = [
    os.environ["SAMS_API_TEST_KEY"],
]

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or unauthorized API key",
    )


@app.get("/scrape")
def scrape(url: str, api_key: str = Security(get_api_key)):
    out = asyncio.run(run.run(url))
    return out