from fastapi import FastAPI
from env import SecurityEnv
from models import Action, StepResponse

app = FastAPI()
env = SecurityEnv()

@app.post("/reset")
async def reset(): return env.reset()

@app.post("/step", response_model=StepResponse)
async def step(action: Action):
    obs, reward, done = env.step(action)
    return {"observation": obs, "reward": reward, "done": done}

@app.get("/state")
async def state(): return {"status": "active"}

@app.get("/")
async def root(): return {"message": "Security Auditor API Running"}