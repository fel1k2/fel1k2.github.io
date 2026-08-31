from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import os
from typing import Optional


class BlockBotsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        blocked_paths = ['.env', '.git', 'wp-admin', 'phpmyadmin', 'backup']
        if any(path in request.url.path.lower() for path in blocked_paths):
            return Response(status_code=404)
        return await call_next(request)


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(BlockBotsMiddleware)


templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, name='index.html', context={"request": request})
