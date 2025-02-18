from contextlib import asynccontextmanager
from aiogram.types import Update
from fastapi import FastAPI, Request
from src.clients import bot, dp
from src.config import settings
from src.handlers import handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    dp.include_router(handler)

    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != settings.WEBHOOK_URL:
        await bot.set_webhook(url=settings.WEBHOOK_URL, allowed_updates=dp.resolve_used_update_types(), drop_pending_updates=True)
    yield
    await bot.session.close()


app = FastAPI(lifespan=lifespan)

@app.post('/webhook')
async def webhook(request:Request):
    telegram_update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, telegram_update)


