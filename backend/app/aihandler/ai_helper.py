from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key="sk-proj-KM7jEYCq22ckCPfnJBTkT3BlbkFJ0WQDyU3p4oTGyhI1kWls")



async def get_llm_response(query: str):
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ],
        model="gpt-3.5-turbo",
        seed=os.getenv("OPENAI_SEED"),
    )
    return response.choices[0].message.content

async def get_response(query: str):
    response = await get_llm_response(query)
    return {"message" : response}