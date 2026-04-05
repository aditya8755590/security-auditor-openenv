import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://aditya875590-security-auditor-openenv.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "security-auditor-v1")
HF_TOKEN = os.getenv("HF_TOKEN") 

# Required OpenAI client initialization
client = OpenAI(base_url=f"{API_BASE_URL}/v1", api_key=HF_TOKEN if HF_TOKEN else "sim")

def run():
    print("START")
    requests.post(f"{API_BASE_URL}/reset")
    print("STEP")
    requests.post(f"{API_BASE_URL}/step", json={"command": "LIST_FILES", "target": ""})
    print("END")

if __name__ == "__main__":
    run()