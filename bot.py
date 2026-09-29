"""
bot.py - Main entry point for the Telegram bot
Handles Bot initialization, Dispatcher setup, error handlers, and polling.
"""

import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, ErrorEvent
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, LOG_LEVEL
from handlers import router

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("TelefonOlxBot")


async def setup_bot_commands(bot: Bot):
    """Register menu commands visible in Telegram chat interface"""
    commands = [
        BotCommand(command="start", description="🏠 Bosh menyu / Qidiruvni boshlash"),
        BotCommand(command="help", description="📖 Qo'llanma va yordam"),
    ]
    await bot.set_my_commands(commands)
    logger.info("Bot commands successfully registered")


async def main():
    """Main startup coroutine"""
    if not BOT_TOKEN or ":" not in BOT_TOKEN:
        logger.error("Invalid BOT_TOKEN configured. Please verify .env file.")
        sys.exit(1)

    logger.info("Initializing Bot and Dispatcher...")
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Include routers
    dp.include_router(router)

    # Global Error Handler
    @dp.error()
    async def global_error_handler(event: ErrorEvent):
        logger.exception(f"Unhandled error while processing update {event.update}: {event.exception}")
        try:
            if event.update.message:
                await event.update.message.answer(
                    "⚠️ <i>Kechirasiz, ma'lumotni yuklashda qisqa uzilish bo'ldi. Iltimos, qayta urinib ko'ring.</i>",
                    parse_mode="HTML"
                )
            elif event.update.callback_query:
                await event.update.callback_query.answer(
                    "⚠️ Xatolik yuz berdi. Iltimos, birozdan so'ng qayta urinib ko'ring.",
                    show_alert=True
                )
        except Exception:
            pass

    # Drop any pending updates before polling
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_bot_commands(bot)

    me = await bot.get_me()
    logger.info(f"Bot started successfully! Username: @{me.username} (ID: {me.id})")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        logger.info("Bot session closed safely.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot manually terminated.")
    except Exception as e:
        logger.critical(f"Fatal error in main loop: {e}", exc_info=True)
