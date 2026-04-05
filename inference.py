import os
import requests
from openai import OpenAI

# 1. Checklist Variables (Strictly for the LLM)
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN") # No default here, as required!

# 2. Configure OpenAI client using exactly those variables
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN if HF_TOKEN else "sim-key"
)

# 3. Your specific Environment URL
ENV_URL = "https://aditya875590-security-auditor-openenv.hf.space"

def run_agent():
    print("START") # Required structured format
    
    # Reset Environment
    requests.post(f"{ENV_URL}/reset")
    
    print("STEP") # Required structured format
    
    # Simulation: Agent decides to look at files
    requests.post(f"{ENV_URL}/step", json={"command": "LIST_FILES", "target": ""})
    
    print("END") # Required structured format

if __name__ == "__main__":
    run_agent()
