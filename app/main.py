from fastapi import FastAPI,Request
from app.routes.routes import router
from fastapi.openapi.utils import get_openapi
from fastapi_users.router import get_oauth_router
from app.auth.ggl_oauth import google_oauth_client, google_auth_backend
from app.config import SECRET
from app.auth.user_manager import get_user_manager
from app.config import REDIRECT_URI
from fastapi.responses import RedirectResponse


from httpx_oauth.clients.google import GoogleOAuth2

original_get_id_email = GoogleOAuth2.get_id_email

async def debug_get_id_email(self, token):
    try:
        return await original_get_id_email(self, token)
    except Exception as e:
        print("Error in get_id_email:", e)
        raise e

GoogleOAuth2.get_id_email = debug_get_id_email




app=FastAPI()

def get_login_redirect(request, user):
    return RedirectResponse(url="http://localhost:5173/success")

app.include_router(router)
app.include_router(get_oauth_router(
    oauth_client=google_oauth_client,
    backend=google_auth_backend,
    state_secret=SECRET,
    get_user_manager=get_user_manager,
    redirect_url="http://localhost:5173/success",
    
    ),
    prefix="/auth/google",
    tags=["auth"]
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Reverbia API",
        version="1.0.0",
        description="API for the audio app",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    app.openapi_schema["security"] = [{"bearerAuth": []}]
    return app.openapi_schema

app.openapi = custom_openapi



@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def main():
    return {"Response":"Hello! This works"}