import os
from pathlib import Path
from dotenv import load_dotenv

# load .env from this folder
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME       = os.getenv("DB_NAME", "aagaaram_db")
SECRET_KEY    = os.getenv("SECRET_KEY", "change-me")
