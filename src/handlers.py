from aiogram import Router
from aiogram.types import  Message, BufferedInputFile
from aiogram.filters import CommandStart, Command
from aiogram.utils.formatting import Text
from src.config import settings
from src.uml import generator
from src.clients import generate_content, parse_content
handler = Router()

@handler.message(CommandStart())
async def start_command(message: Message):
    welcome = Text("""# PlantUML Bot
This is a bot to help generate UML Diagrams, by using [PlantUML](https://plantuml.com/en/) Code. Just send code to bot and get UML Diagram:
```
@startuml
Bob -> Alice : hello
@enduml
```
You also can use Google Gemini to ask for generation, just use command /ask "prompt".""")
    await message.answer(welcome.as_markdown(), parse_mode="MarkdownV2")

@handler.message(Command("help"))
async def help_command(message: Message):
    welcome = Text("""# PlantUML Bot
    This is a bot to help generate UML Diagrams, by using [PlantUML](https://plantuml.com/en/) Code. Just send code to bot and get UML Diagram:
    ```
    @startuml
    Bob -> Alice : hello
    @enduml
    ```
    You also can use Google Gemini to ask for generation, just use command /ask "prompt".""")
    await message.answer(welcome.as_markdown(), parse_mode="MarkdownV2")

@handler.message(lambda x: x.text.startswith("@startuml"))
async def uml_command(message: Message):
    try:
        image = await generator.process(message.text)
        await message.answer_photo(image)
    except Exception as e:
        await message.answer(f"Error: {e}")

@handler.message(Command("ask"))
async def ask_command(message: Message):
    text = message.text[4:] # remove /ask command from message
    if len(text) < settings.MIN_ASK_LENGTH:
        await message.answer(f"Very short prompt, it should be at least {settings.MIN_ASK_LENGTH} characters long")
    else:
        await message.answer("Generation ...")
        gemini_content = []
        async for t in generate_content(text):
            gemini_content.append(t)
        uml_code = parse_content(" ".join(gemini_content))
        await message.answer(uml_code)
        try:
            image = await generator.process(uml_code)
            await message.answer_photo(image)
        except Exception as e:
            await message.answer(f"Error: {e}")

@handler.message()
async def echo_all(message: Message):
    await message.answer(f"Can`t understand")