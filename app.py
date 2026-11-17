import os, json
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI

ROOT = Path(__file__).parent
MEMORY_FILE = ROOT / "memory.json"
app = FastAPI(title="BuildMaster AI")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"preferences": [], "decisions": [], "ideas": []}

def save_memory(data):
    MEMORY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

class ChatInput(BaseModel):
    message: str

@app.get("/")
def home():
    return FileResponse(ROOT / "static" / "index.html")

@app.get("/api/health")
def health():
    return {"ok": True, "ai_configured": bool(os.getenv("OPENAI_API_KEY"))}

@app.get("/api/memory")
def memory():
    return load_memory()

@app.post("/api/chat")
def chat(payload: ChatInput):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return {"reply": "BuildMaster AI is ready, but its AI connection is not configured yet. Add OPENAI_API_KEY in your hosting environment to enable AI replies.", "memory": load_memory()}
    memory = load_memory()
    client = OpenAI(api_key=key)
    instructions = (
        "You are BuildMaster AI, a patient personal software-building partner. "
        "Understand plain-language requests, explain simply, and help plan and create software. "
        "Do not claim you executed, tested, or deployed anything unless it actually happened. "
        "Ask only essential questions. Respect the user's project boundaries. "
        "The user prefers simple Roman Pashto and concise step-by-step guidance. "
        "NeedBridge is a separate project and must never be changed unless explicitly authorized."
    )
    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5"),
            instructions=instructions + "\nApproved user memory:\n" + json.dumps(memory, ensure_ascii=False),
            input=payload.message
        )
        return {"reply": response.output_text, "memory": memory}
    except Exception as e:
        return {"reply": "AI connection error. Check the API key, model access, and hosting logs. (" + str(e)[:180] + ")", "memory": memory}

@app.post("/api/memory")
def update_memory(data: dict):
    allowed = {"preferences", "decisions", "ideas"}
    current = load_memory()
    for key in allowed:
        if key in data and isinstance(data[key], list):
            current[key] = data[key][:100]
    save_memory(current)
    return {"ok": True, "memory": current}
