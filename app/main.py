from fastapi import FastAPI
from app.auth.custom_auth import custom_auth_router
from app.routes.routes import router

app=FastAPI()

app.include_router(router)

from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response



@app.get("/")
def main():
    return {"Response":"Hello! This works"}