import aiohttp

from schemas import User

BASE_URL = "http://127.0.0.1:8443"


async def get_user_by_telegram_id(telegram_id: int):
    async with aiohttp.ClientSession() as session:
        params = {"telegram_id": telegram_id}
        async with session.get(f"{BASE_URL}/users", params=params) as response:
            return await response.json()


async def add_user(user: User):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BASE_URL}/users", json=user.model_dump()
        ) as response:
            return await response.json()


async def generate_image(image_path: str, prompt: str):
    async with aiohttp.ClientSession() as session:
        data = {"image_path": image_path, "prompt": prompt}
        async with session.post(f"{BASE_URL}/images/generate", json=data) as response:
            return await response.json()
