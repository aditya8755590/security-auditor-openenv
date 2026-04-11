import os
import requests
from openai import OpenAI

# 1. Strict Environment Variables (From Meta Guidelines)
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "sim-key") 

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

# URL for the local FastAPI server
ENV_URL = "http://localhost:7860" 

def run_agent():
    tasks = ["Task_1_Easy", "Task_2_Medium", "Task_3_Hard"]
    
    for task_name in tasks:
        # 🚨 STRICT LOG 1: [START]
        print(f"[START] task={task_name} env=AlgorithmicDebugger model={MODEL_NAME}", flush=True)
        
        # Reset Environment
        try:
            res = requests.post(f"{ENV_URL}/reset", json={"task_name": task_name}).json()
            buggy_code = res.get("code", "")
        except Exception:
            # STRICT BOUNDARY: 0.01 instead of 0.0
            print(f"[END] success=false steps=0 rewards=0.01", flush=True)
            continue

        step_count = 0
        rewards_history = []
        is_success = False
        done = False

        # Agent Loop (Max 3 attempts per task)
        while not done and step_count < 3:
            step_count += 1
            step_error = "null"
            step_reward = 0.01 # STRICT BOUNDARY
            
            # 1. Ask the LLM to fix the bug (REAL LLM CALL RESTORED)
            try:
                prompt = f"Fix this Python code to pass standard edge cases. Reply ONLY with the exact raw Python code, no markdown:\n\n{buggy_code}"
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300
                )
                fixed_code = completion.choices[0].message.content.strip()
                
                # Strip markdown just in case the LLM disobeys
                if fixed_code.startswith("```python"):
                    fixed_code = fixed_code[9:-3].strip()
            except Exception as e:
                # Silently catch the error so the loop continues mechanically
                fixed_code = buggy_code
                step_error = "llm_failure"

            # 2. Action: Apply the Patch
            try:
                requests.post(f"{ENV_URL}/step", json={"command": "APPLY_PATCH", "target": fixed_code})
                
                # 3. Action: Run the hidden Tests
                step_res = requests.post(f"{ENV_URL}/step", json={"command": "RUN_TESTS", "target": ""}).json()
                step_reward = step_res.get("reward", 0.01)
                done = step_res.get("done", False)
            except Exception:
                step_error = "env_step_failed"
                done = True

            rewards_history.append(str(float(step_reward)))

            # STRICT BOUNDARY: Check for 0.90 instead of 1.0
            if step_reward >= 0.90:
                is_success = True

            # 🚨 STRICT LOG 2: [STEP]
            print(f"[STEP] step={step_count} action=RUN_TESTS reward={step_reward:.2f} done={str(done).lower()} error={step_error}", flush=True)

        # 🚨 STRICT LOG 3: [END]
        rewards_str = ",".join(rewards_history)
        print(f"[END] success={str(is_success).lower()} steps={step_count} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    run_agent()