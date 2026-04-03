import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret-key")
    GEMINI_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    LLM_MODEL_NAME: str = "gemini-3-flash-preview"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 12 * 60
    DATABASE_URL: str = "sqlite:///database.db"


settings = Settings()
