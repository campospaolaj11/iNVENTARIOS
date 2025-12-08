from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_SERVER: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_DRIVER: str = "ODBC Driver 17 for SQL Server"
    
    # API
    SECRET_KEY: str
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173"
    
    @property
    def database_url(self) -> str:
        """Genera la cadena de conexión para SQL Server"""
        return (
            f"mssql+pyodbc://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_SERVER}/{self.DATABASE_NAME}"
            f"?driver={self.DATABASE_DRIVER.replace(' ', '+')}"
        )
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
