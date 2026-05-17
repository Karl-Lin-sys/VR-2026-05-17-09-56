from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from ai_core import generate_response
from security import validate_input, filter_output, authenticate_user
from self_regulation import SelfRegulationSystem

app = FastAPI(title="VR AI Russian Girlfriend Backend")

# CORS setup for WebXR frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize self-regulation system
regulation_system = SelfRegulationSystem()

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    emotion: str
    action: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # 1. Security: Authentication
    if not authenticate_user(request.user_id):
        raise HTTPException(status_code=403, detail="Unauthorized user. I only talk to my Master.")

    # 2. Security: Input Validation (Prompt Injection & Moderation)
    if not validate_input(request.message):
        return ChatResponse(
            reply="ちょっと、何言ってるの？そういうのは好きじゃないわ。",
            emotion="angry",
            action="look_away"
        )

    # 3. Self-Regulation: Pre-processing (Update state based on input)
    current_state = regulation_system.evaluate_input(request.message)

    # 4. AI Core: Generate Response
    ai_reply = generate_response(request.message, current_state)

    # 5. Security: Output Filtering
    safe_reply = filter_output(ai_reply)

    # 6. Self-Regulation: Post-processing (Update state based on output)
    final_emotion, final_action = regulation_system.determine_behavior(safe_reply)

    return ChatResponse(
        reply=safe_reply,
        emotion=final_emotion,
        action=final_action
    )

@app.get("/status")
def get_status():
    return {
        "status": "online",
        "current_state": regulation_system.get_state()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
