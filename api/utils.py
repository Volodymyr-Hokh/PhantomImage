import asyncio

from dotenv import load_dotenv
from gradio_client import Client, handle_file
from openai import AsyncOpenAI


load_dotenv()

client = AsyncOpenAI()


def generate_image(image_path: str, prompt: str):
    client = Client("AP123/IllusionDiffusion")
    result = client.predict(
        control_image=handle_file(image_path),
        prompt=prompt,
        negative_prompt="low quality",
        guidance_scale=7.5,
        controlnet_conditioning_scale=1.1,
        control_guidance_start=0,
        control_guidance_end=1,
        upscaler_strength=1,
        seed=-1,
        sampler="Euler",
        api_name="/inference",
    )
    client.close()
    print(result)
    return result[0]


async def generate_image_async(image_path: str, prompt: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, generate_image, image_path, prompt)


async def translate_message(message):
    task = (
        "Translate the following message into English."
        + "\nIf the message is already in English, please return it as it is."
        + "\nAvoid any self-referential comments like 'Here is a draft message'."
        + '\nDo not use " to highlight the message'
        + "\nExample: Input:'Bonjour' Output:'Hello'"
    )
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": task},
            {"role": "user", "content": message},
        ],
    )
    output_text = response.choices[0].message.content
    return output_text
