"""Configuration management using Pydantic Settings"""

from pydantic_settings import BaseSettings
from pydantic import Field
from datetime import date


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    
    # Redis
    redis_url: str = Field(..., env="REDIS_URL")
    
    # Telegram Bot
    bot_token: str = Field(..., env="BOT_TOKEN")
    webhook_url: str | None = Field(None, env="WEBHOOK_URL")
    webhook_secret: str | None = Field(None, env="WEBHOOK_SECRET")
    
    # FastAPI
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")
    
    # Admin
    admin_api_key: str = Field(..., env="ADMIN_API_KEY")
    
    # Week Calculation
    academic_start_date: date = Field(..., env="ACADEMIC_START_DATE")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
