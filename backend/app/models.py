from pydantic import BaseModel

class Questions(BaseModel):
    query: str
    