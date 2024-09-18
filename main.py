import asyncio
import logging
from os import getenv, chdir
import sys
from uuid import uuid4

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    FSInputFile,
)
from dotenv import load_dotenv

from api_client import (
    add_user,
    get_user_by_telegram_id,
    generate_image,
)
from schemas import User
from api.utils import translate_message
from api.url_parser import update_url

load_dotenv()
# chdir("/root/PhantomImage/")

TOKEN = getenv("BOT_TOKEN")
PAYMENT_PROVIDER_TOKEN = getenv("PAYMENT_PROVIDER_TOKEN")
dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            has_active_subscription=False,
            subscription_end_date=None,
            free_images_left=3,
        )
        await add_user(user)
    await message.answer(
        "Hello! I'm PhantomImage bot. I can generate images from your prompts. Just send me a photo and a prompt and I'll do the rest."
    )


@dp.message(F.photo)
async def photo_handler(message: Message) -> None:
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            has_active_subscription=False,
            subscription_end_date=None,
            free_images_left=3,
        )
        await add_user(user)
    loader_message = None
    try:
        loader_message = await message.answer_animation(
            animation=FSInputFile("loader.gif"),
            caption="Generating image. Please, wait a moment...",
        )
        photo = message.photo[-1]
        caption = message.caption
        prompt = await translate_message(caption)
        file = await bot.get_file(photo.file_id)

        file_path = file.file_path
        file_extension = file_path.split(".")[-1]
        file_id = uuid4()
        destination = f"images/input/{file_id}.{file_extension}"
        await bot.download_file(file_path, destination)

        response = await generate_image(image_path=destination, prompt=prompt)
        image_path = response["result"]
        await message.reply_photo(FSInputFile(image_path))

    except Exception:
        await message.reply(f"Something went wrong. Please, try again later.")

    if loader_message:
        await loader_message.delete()


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
