# BuildMaster AI — Python edition

A starter personal software-building assistant built with FastAPI and a small web interface.

## Run locally
1. Install Python 3.10 or newer.
2. Run `pip install -r requirements.txt`
3. Set `OPENAI_API_KEY` in your environment.
4. Run `uvicorn app:app --host 0.0.0.0 --port 8000`
5. Open `http://localhost:8000`

## Deploy
The included `render.yaml` is a Render Blueprint for a Python web service. A hosting provider may still require identity or payment verification. The app itself does not bypass provider requirements.

## Important
- Never paste API keys into chat or commit them to GitHub.
- Memory is a simple local JSON file in this starter. Free hosts may erase local files or use temporary storage, so this is not yet reliable permanent cross-device memory.
- The AI feature needs an API key and a model your account can access. API usage may cost money.
- Generated code is advice/output only; this starter does not run untrusted generated code or autonomously deploy projects.
- NeedBridge is a separate project and is not included or modified.
