from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from agents.pharmacist import get_pharmacist_response
from utils.database import get_medicine_data, get_order_history, get_proactive_refills
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(title="Agentic Pharmacy System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []

@app.get("/")
def read_root():
    return {"status": "Pharmacy Agent Backend is running"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Convert dict history to LangChain messages
        formatted_history = []
        for msg in request.history:
            if msg['role'] == 'user':
                formatted_history.append(HumanMessage(content=msg['content']))
            else:
                formatted_history.append(AIMessage(content=msg['content']))
        
        response = get_pharmacist_response(request.message, formatted_history)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/inventory")
async def inventory():
    df = get_medicine_data()
    return df.to_dict(orient='records')

@app.get("/history")
async def history():
    df = get_order_history()
    return df.to_dict(orient='records')

@app.get("/alerts")
async def alerts():
    proactive_alerts = get_proactive_refills()
    return proactive_alerts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
