import os
import requests

# MATCHING THE SCALER CHECKLIST EXACTLY
API_BASE_URL = os.getenv("API_BASE_URL", "https://aditya875590-security-auditor-openenv.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "security-auditor-v1")
HF_TOKEN = os.getenv("HF_TOKEN") # No default here as per checklist

def run_agent():
    print("START") # Required structured format
    
    # 1. Reset
    requests.post(f"{API_BASE_URL}/reset")
    
    # 2. Example Step (List Files)
    print("STEP") # Required structured format
    response = requests.post(
        f"{API_BASE_URL}/step", 
        json={"command": "LIST_FILES", "target": ""}
    )
    print(f"Action: LIST_FILES | Observation: {response.json()['observation']['system_message']}")
    
    print("END") # Required structured format

if __name__ == "__main__":
    run_agent()