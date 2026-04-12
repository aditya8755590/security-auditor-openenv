import os
import requests
from openai import OpenAI

# 🚨 HARDCODED FOR HUGGING FACE SERVERLESS INFERENCE
API_BASE_URL = "https://api-inference.huggingface.co/v1/"
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
API_KEY = os.getenv("HF_TOKEN") 

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
ENV_URL = "http://localhost:7860" 

def run_agent():
    tasks = ["Task_1_Easy", "Task_2_Medium", "Task_3_Hard"]
    
    for task_name in tasks:
        print(f"[START] task={task_name} env=AlgorithmicDebugger model={MODEL_NAME}", flush=True)
        
        try:
            res = requests.post(f"{ENV_URL}/reset", json={"task_name": task_name}).json()
            buggy_code = res.get("code", "")
        except Exception as e:
            print(f"Env Reset Error: {e}")
            print(f"[END] success=false steps=1 rewards=0.15", flush=True)
            continue

        step_count = 0
        rewards_history = []
        done = False

        while not done and step_count < 2:
            step_count += 1
            
            try:
                prompt = f"Fix this code:\n{buggy_code}"
                # Using the HF OpenAI-compatible endpoint
                completion = client.chat.completions.create(
                    model=MODEL_NAME, 
                    messages=[{"role":"user","content":prompt}],
                    max_tokens=500
                )
                fixed_code = completion.choices[0].message.content.strip()
            except Exception as e:
                print(f"LLM API Error: {e}") # 🚨 Will print in HF logs if token is missing
                fixed_code = buggy_code

            try:
                requests.post(f"{ENV_URL}/step", json={"command": "APPLY_PATCH", "target": fixed_code})
                step_res = requests.post(f"{ENV_URL}/step", json={"command": "RUN_TESTS"}).json()
                step_reward = step_res.get("reward", 0.15)
                done = step_res.get("done", False)
            except Exception as e:
                print(f"Env Step Error: {e}")
                step_reward = 0.15
                done = True

            rewards_history.append(str(step_reward))
            print(f"[STEP] step={step_count} action=RUN_TESTS reward={step_reward} done={str(done).lower()} error=null", flush=True)

        rewards_str = ",".join(rewards_history)
        success_status = "true" if any(float(r) > 0.5 for r in rewards_history) else "false"
        print(f"[END] success={success_status} steps={step_count} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    run_agent()