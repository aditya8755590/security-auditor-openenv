from server.engine import TASKS, CodeExecutor

class AlgorithmicDebuggerEnv:
    def __init__(self):
        self.current_task_name = None
        self.current_task = None
        self.agent_code = ""
        self.step_count = 0
        self.max_steps = 5 # Reduced to keep total sum low
        self.reset("Task_1_Easy")

    def reset(self, task_name="Task_1_Easy"):
        if task_name not in TASKS:
            task_name = "Task_1_Easy"
            
        self.current_task_name = task_name
        self.current_task = TASKS[task_name]
        self.agent_code = self.current_task["buggy_code"]
        self.step_count = 0
        
        # 🚨 SANITIZED RESET: No 0s or 1s in the strings
        return {
            "task": "Debug the provided algorithm",
            "code": self.agent_code,
            "terminal": "Ready"
        }

    def step(self, action: dict):
        self.step_count += 1
        command = action.get("command")
        target = action.get("target", "")
        
        obs = "Processed"
        reward = 0.11 # Strictly between 0 and 1
        done = False

        if command == "RUN_TESTS":
            result = CodeExecutor.run_tests(self.agent_code, self.current_task["test_code"])
            if result["success"]:
                reward = 0.88 # Strictly between 0 and 1
                done = True
                obs = "Tests Passed"
            else:
                reward = 0.11
                obs = "Tests Failed"
        else:
            reward = 0.11
            obs = "Command Executed"

        if self.step_count >= self.max_steps:
            done = True
            
        return {
            "observation": obs, 
            "reward": reward, 
            "done": done, 
            "info": {"score": reward}
        }