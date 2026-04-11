from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from server.env import AlgorithmicDebuggerEnv

app = FastAPI(title="Algorithmic Debugger OpenEnv")

# Initialize our new real-execution environment
env = AlgorithmicDebuggerEnv()

# 🛡️ Pydantic Models for Strict Spec Compliance
class Action(BaseModel):
    command: str
    target: Optional[str] = ""

class ResetRequest(BaseModel):
    task_name: Optional[str] = "Task_1_Easy"

@app.get("/")
def read_root():
    return {"status": "Algorithmic Debugger is Running"}

@app.post("/reset")
def reset_env(req: ResetRequest = None):
    # Route the specific Easy/Medium/Hard task to the engine
    task = req.task_name if req else "Task_1_Easy"
    obs = env.reset(task)
    return {
        "observation": obs["terminal"], 
        "code": obs["code"], 
        "task": obs["task"]
    }

@app.post("/step")
def step_env(action: Action):
    # Pass the strict Pydantic action to the engine
    result = env.step(action.model_dump())
    return result

@app.get("/state")
def get_state():
    return {
        "task": env.current_task_name,
        "step_count": env.step_count,
        "code_state": env.agent_code
    }