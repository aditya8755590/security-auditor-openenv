import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "sim-key") 

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
ENV_URL = "http://localhost:7860" 

def run_agent():
    tasks = ["Task_1_Easy", "Task_2_Medium", "Task_3_Hard"]
    
    for task_name in tasks:
        print(f"[START] task={task_name} env=AlgorithmicDebugger model={MODEL_NAME}", flush=True)
        
        try:
            res = requests.post(f"{ENV_URL}/reset", json={"task_name": task_name}).json()
            buggy_code = res.get("code", "")
        except Exception:
            print(f"[END] success=false steps=0 rewards=0.01", flush=True)
            continue

        step_count = 0
        rewards_history = []
        is_success = False
        done = False

        while not done and step_count < 3:
            step_count += 1
            step_error = "null"
            step_reward = 0.01
            
            try:
                prompt = f"Fix this Python code to pass standard edge cases. Reply ONLY with the exact raw Python code, no markdown:\n\n{buggy_code}"
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300
                )
                fixed_code = completion.choices[0].message.content.strip()
                if fixed_code.startswith("```python"):
                    fixed_code = fixed_code[9:-3].strip()
            except Exception:
                fixed_code = buggy_code
                step_error = "llm_failure"

            try:
                requests.post(f"{ENV_URL}/step", json={"command": "APPLY_PATCH", "target": fixed_code})
                step_res = requests.post(f"{ENV_URL}/step", json={"command": "RUN_TESTS", "target": ""}).json()
                step_reward = step_res.get("reward", 0.01)
                done = step_res.get("done", False)
            except Exception:
                step_error = "env_step_failed"
                done = True

            rewards_history.append(str(float(step_reward)))
            
            if step_reward >= 0.90:
                is_success = True

            # 🚨 REMOVED the .2f formatting that caused the 0.00 bug
            print(f"[STEP] step={step_count} action=RUN_TESTS reward={step_reward} done={str(done).lower()} error={step_error}", flush=True)

        rewards_str = ",".join(rewards_history)
        print(f"[END] success={str(is_success).lower()} steps={step_count} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    run_agent()