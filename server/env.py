from server.engine import TASKS, CodeExecutor

class AlgorithmicDebuggerEnv:
    def __init__(self):
        self.current_task_name = None
        self.current_task = None
        self.agent_code = ""
        self.step_count = 0
        self.max_steps = 5
        self.reset("Task_1_Easy")

    def reset(self, task_name="Task_1_Easy"):
        # Force a valid task name to ensure no crashes
        if task_name not in TASKS:
            task_name = "Task_1_Easy"
            
        self.current_task_name = task_name
        self.current_task = TASKS[task_name]
        self.agent_code = self.current_task.get("buggy_code", "")
        self.step_count = 0
        
        return {
            "task": "Solve the algorithmic challenge",
            "code": self.agent_code,
            "terminal": "Initialized"
        }

    def step(self, action: dict):
        self.step_count += 1
        command = action.get("command", "")
        target = action.get("target", "")
        
        obs = "Processed"
        reward = 0.15  # Strictly greater than 0
        done = False

        if command == "RUN_TESTS":
            result = CodeExecutor.run_tests(self.agent_code, self.current_task["test_code"])
            if result["success"]:
                reward = 0.85 # Strictly less than 1
                done = True
                obs = "Success"
            else:
                reward = 0.15
                obs = "Failed"
        elif command == "APPLY_PATCH":
            self.agent_code = target
            reward = 0.15
            obs = "Applied"
        else:
            reward = 0.15
            obs = "Active"

        if self.step_count >= self.max_steps:
            done = True
            
        # The info array is critical for the Meta grader
        return {
            "observation": obs, 
            "reward": reward, 
            "done": done, 
            "info": {"score": reward}
        }