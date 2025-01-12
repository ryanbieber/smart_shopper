"""Settings File for Nostradamus."""
from __future__ import annotations

import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Base settings for the Nostradamus app."""
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")

    class Config:
        env_file = "/home/carnufex/smart_shopper/config/secrets"



settings = Settings()