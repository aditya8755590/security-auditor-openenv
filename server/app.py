from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from env import SecurityEnv
from models import Action, StepResponse

app = FastAPI()
env = SecurityEnv()

@app.post("/reset")
async def reset():
    return env.reset()

@app.post("/step", response_model=StepResponse)
async def step(action: Action):
    obs, reward, done = env.step(action)
    return {"observation": obs, "reward": reward, "done": done}

@app.get("/state")
async def state():
    # Meta requires a way to check if the env is healthy
    return {"status": "active", "current_view": env.current_view}

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Security Auditor Environment</title>
            <style>
                body { background-color: #0d1117; color: #c9d1d9; font-family: -apple-system, sans-serif; text-align: center; padding-top: 100px; }
                h1 { color: #58a6ff; }
                .btn { background-color: #238636; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-size: 18px; display: inline-block; margin-top: 20px; transition: 0.2s; }
                .btn:hover { background-color: #2ea043; }
            </style>
        </head>
        <body>
            <h1>🛡️ Security Auditor OpenEnv</h1>
            <p>Advanced Multi-Step RL Environment for AI Agents.</p>
            <p>System Status: <strong>ONLINE</strong></p>
            <a href="/docs" class="btn">🚀 Enter Interactive API Dashboard</a>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

def run_server():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)