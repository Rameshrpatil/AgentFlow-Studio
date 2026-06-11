from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Load explicitly just in case
load_dotenv()

class Settings(BaseSettings):
    EXECUTION_MODE: str = os.getenv("EXECUTION_MODE", "mock")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    class Config:
        env_file = ".env"

settings = Settings()
