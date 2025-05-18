import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
SECRET=os.getenv("SECRET")
SYNCED_DB_URL=os.getenv("SYNCED_DB_URL")



