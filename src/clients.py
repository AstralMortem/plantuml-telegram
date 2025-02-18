from aiogram import Bot, Dispatcher
from google import genai
from google.genai.types import GenerateContentConfig
from src.config import settings
import re


bot = Bot(token=settings.BOT_API_TOKEN)
dp = Dispatcher()
gemini = genai.Client(api_key=settings.GEMINI_API_TOKEN)


async def generate_content(prompt: str):
    response = gemini.models.generate_content_stream(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=GenerateContentConfig(
            system_instruction=settings.GEMINI_SYSTEM_INSTRUCTION
        )
    )
    for resp in response:
        yield resp.text

def parse_content(prompt: str):
    pattern = r'@startuml(.*?)@enduml'
    matches = re.findall(pattern, prompt, re.DOTALL)  # re.DOTALL allows dot (.) to match newlines
    return f"@startuml\n{matches[0]}\n@enduml"
