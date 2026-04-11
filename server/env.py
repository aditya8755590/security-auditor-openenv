from server.engine import TASKS, CodeExecutor

class AlgorithmicDebuggerEnv:
    def __init__(self):
        self.current_task_name = None
        self.current_task = None
        self.agent_code = ""
        self.step_count = 0
        self.max_steps = 10
        self.reset("Task_1_Easy")

    def reset(self, task_name="Task_1_Easy"):
        if task_name not in TASKS:
            task_name = "Task_1_Easy"
            
        self.current_task_name = task_name
        self.current_task = TASKS[task_name]
        self.agent_code = self.current_task["buggy_code"]
        self.step_count = 0
        
        return {
            "task": self.current_task["description"],
            "code": self.agent_code,
            "terminal": "System initialized. Waiting for action."
        }

    def step(self, action: dict):
        self.step_count += 1
        command = action.get("command")
        target = action.get("target", "")
        
        obs = ""
        reward = 0.01
        done = False

        if command == "READ_CODE":
            obs = self.agent_code
            reward = 0.01
            
        elif command == "APPLY_PATCH":
            self.agent_code = target
            obs = "Patch applied. Run tests to verify."
            reward = 0.01
            
        elif command == "RUN_TESTS":
            result = CodeExecutor.run_tests(self.agent_code, self.current_task["test_code"])
            obs = result["output"]
            
            if result["success"]:
                reward = 0.90
                done = True
                obs += "\n\nSUCCESS! All tests passed."
            else:
                reward = 0.01
                obs += "\n\nFAILED. Check the stack trace."
                
        else:
            obs = "Invalid command."
            reward = 0.01

        if self.step_count >= self.max_steps:
            done = True
            
        # 🚨 BULLETPROOF ADDITION: Meta looks for an info['score'] key
        return {
            "observation": obs, 
            "reward": reward, 
            "done": done, 
            "info": {"score": reward}
        }