from secrets import token_urlsafe
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI(
    title="Url Shortener API"
)

url_store: dict[str, str] = {}

class URLRequest(BaseModel):
    url: HttpUrl

@app.post("/shorten")
def shorten_url(request: URLRequest):
    original_url = str(request.url)

    while True:
        short_code = token_urlsafe(5)

        if short_code not in url_store:
            break

    url_store[short_code] = original_url

    return {
        'original_url': original_url,
        'short_code': short_code,
        'short_url': f'/r/{short_code}',
    }

@app.get('/r/{short_code}')
def redirect_to_original(short_code: str):
    original_url = url_store.get(short_code)

    if original_url is None: 
        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )

    return RedirectResponse(
        url=original_url,
        status_code=307,
    )