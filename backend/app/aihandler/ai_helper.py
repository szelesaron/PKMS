from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv(".env")


client = AsyncOpenAI(api_key = os.getenv("OPENAI_API_KEY"))



async def get_llm_response(query: str):
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ],
        model="gpt-3.5-turbo",
        seed=int(os.getenv("OPENAI_SEED")),
    )
    return response.choices[0].message.content

async def get_response(query: str):
    response = await get_llm_response(query)
    print(response)
    return {"message" : response}