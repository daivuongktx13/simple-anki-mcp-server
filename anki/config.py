from pydantic import BaseModel, Field
import os

class Settings(BaseModel):
    anki_base_url: str = Field(default=os.getenv("ANKI_URL", "http://127.0.0.1:8765"))
    anki_api_key: str = Field(default=os.getenv("ANKI_KEY", None))
    anki_timeout: str = Field(default=float(os.getenv("ANKI_TIMEOUT", "10")))


settings = Settings()