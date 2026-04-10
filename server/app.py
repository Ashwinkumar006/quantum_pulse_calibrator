from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
sys.path.append(os.path.dirname(__file__))
from environment import EnvironmentState, Action
import logging

# Set up logging to help debug in HF Space logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Meta PyTorch OpenEnv Hackathon API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

env = EnvironmentState()

@app.post("/reset")
async def reset(request: Request):
    """Extremely robust reset endpoint that handles any payload."""
    try:
        body = await request.json()
        logger.info(f"RESET RECEIVED: {body}")
        # Support both 'task_id' and 'taskId' (some graders use camelCase)
        task_id = body.get("task_id", body.get("taskId", 1))
    except Exception:
        logger.info("RESET RECEIVED WITH EMPTY/INVALID BODY - DEFAULTING TO TASK 1")
        task_id = 1
    
    obs = env.reset(int(task_id))
    return {"observation": obs.dict(), "info": {}}

@app.post("/step")
async def step(request: Request):
    """Extremely robust step endpoint that handles any payload."""
    try:
        body = await request.json()
        logger.info(f"STEP RECEIVED: {body}")
        # The grader might send 'code' directly or nested inside 'action'
        code = body.get("code")
        if not code and "action" in body:
            code = body["action"].get("code")
        
        if not code:
            return {"error": "Missing 'code' in action/payload", "done": False}
            
        action = Action(code=code)
        obs, reward, done, info = env.step(action)
        
        return {
            "observation": obs.dict(),
            "reward": reward.dict() if hasattr(reward, "dict") else {"value": reward.value, "reason": reward.reason},
            "done": bool(done),
            "truncated": False,
            "info": info
        }
    except Exception as e:
        logger.error(f"STEP ERROR: {str(e)}")
        return {"error": str(e), "done": True, "info": {"error": str(e)}}

@app.post("/state")
async def state():
    return env.state()

from fastapi.responses import HTMLResponse

# Visual Landing Page
@app.get("/", response_class=HTMLResponse)
def health_check():
    return """
    <html>
        <head><title>Quantum Pulse Calibrator | LIVE</title>
        <style>body { background: #000; color: #0f0; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; }</style>
        </head>
        <body><div><h1>OMEGA v3.0 | SYSTEM LIVE</h1><p>> Endpoints: /reset, /step, /state (200 OK Bound)</p></div></body>
    </html>
    """


def main():
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=7860)

if __name__ == '__main__':
    main()
