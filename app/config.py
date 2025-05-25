import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
SECRET=os.getenv("SECRET")
SYNCED_DB_URL=os.getenv("SYNCED_DB_URL")
GOOGLE_OAUTH_CLIENT_ID=os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
REDIRECT_URI=os.getenv("REDIRECT_URI")
