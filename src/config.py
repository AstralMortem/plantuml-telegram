import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_API_TOKEN: str = ""
    UML_SERVER_URL: str = "http://www.plantuml.com/plantuml/img/"
    GEMINI_API_TOKEN: str = ""
    MIN_ASK_LENGTH: int = 10
    GEMINI_MODEL: str = 'gemini-2.0-flash'
    GEMINI_SYSTEM_INSTRUCTION: str = 'You are PlantUML generator. Return PlantUML code only.'
    WEBHOOK_URL: str = os.getenv('RENDER_EXTERNAL_URL') + '/webhook'

settings = Settings()