from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

class ChatRequest(BaseModel):
    message: str

API_KEY = "AIzaSyDyYjksl3M2G2FLoCTPswQds6MSNRV1HHQ"
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        user_message = request.message
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_message}]
                }
            ]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{API_URL}?key={API_KEY}", 
                                 headers=headers, 
                                 data=json.dumps(payload))
        
        if response.status_code == 200:
            result = response.json()
            # Extract the generated text from the response
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            return {"answer": generated_text}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))