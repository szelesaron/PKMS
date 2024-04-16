from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
from app.models import Questions  
from app.aihandler.ai_helper import get_response, get_llm_response

app = FastAPI()  
  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=["*"],  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)  
  
@app.post("/")
async def create_item(question: Questions):
    # Process the data and return a response
    if question.query:
        response = await get_response(question.query)
        return response
    else:
        raise HTTPException(status_code=400, detail="Name not provided")
    

