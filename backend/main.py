from fastapi import FastAPI, HTTPException  
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel  
  
app = FastAPI()  
  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=["*"],  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)  
  
class Name(BaseModel):  
    name: str  
  
@app.post("/")  
async def create_item(item: Name):  
    # Process the data and return a response  
    if item.name:  
        return {"message": f"Hello, {item.name}!"}  
    else:  
        raise HTTPException(status_code=400, detail="Name not provided")  
  
@app.get("/")  
def read_root():  
    return {"Hello": "World"}  
