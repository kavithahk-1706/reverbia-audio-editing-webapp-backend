
from app.config import GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET
from httpx_oauth.clients.google import GoogleOAuth2
from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from app.auth.custom_auth import get_jwt_strategy








cookie_transport=CookieTransport(cookie_name="reverbia_session",cookie_max_age=3600)

google_oauth_client=GoogleOAuth2(
    client_id=GOOGLE_OAUTH_CLIENT_ID, 
    client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
    scopes=["openid","email","profile"]
    
)

google_auth_backend=AuthenticationBackend(
    name="google",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)


    



    

