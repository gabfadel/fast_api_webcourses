import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "YOUR_RANDOM_SECRET_KEY")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "db")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "mydatabase")

    DATABASE_URL = (
         f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}"
         f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )