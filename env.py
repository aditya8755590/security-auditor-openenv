import numpy as np
from models import Observation, Action

class SecurityEnv:
    def __init__(self):
        self.file_system = {
            "main.py": "import os\nfrom auth import login\nfrom utils import process_data...",
            "auth.py": "def login(user, pwd):\n    if user == 'admin': return True # 🔥 AUTH BYPASS",
            "db.py": "query = 'SELECT * FROM users WHERE email = ' + email # 🔥 SQLi",
            "settings.py": "api_key = 'sk_test_123456' # 🔥 HARDCODED SECRET",
            "worker.py": "while True: continue # 🔥 INFINITE LOOP",
            "leak.cpp": "int* x = new int(10); # 🔥 MEMORY LEAK",
            "utils.py": "obj = pickle.loads(data) # 🔥 RCE",
            "deploy.py": "os.system('git checkout ' + branch) # 🔥 CMD INJECTION"
        }
        self.actual_bugs = {
            "db.py": "SQL_INJECTION", "auth.py": "AUTH_BYPASS",
            "settings.py": "HARDCODED_SECRET", "worker.py": "INFINITE_LOOP",
            "leak.cpp": "MEMORY_LEAK", "utils.py": "UNSAFE_DESERIALIZATION",
            "deploy.py": "COMMAND_INJECTION"
        }
        self.flagged_bugs = set()
        self.current_view = ""
        self.system_msg = ""
        
    def reset(self):
        self.flagged_bugs = set()
        self.current_view = "root"
        self.system_msg = "Environment initialized. PR is open."
        return self._get_obs()

    def _get_obs(self):
        return Observation(
            current_directory="root", available_files=list(self.file_system.keys()),
            file_content_view=self.current_view, bugs_flagged_count=len(self.flagged_bugs),
            system_message=self.system_msg
        )

    def step(self, action: Action):
        reward, done = 0.0, False
        cmd, target = action.command, action.target
        
        if cmd == "LIST_FILES":
            self.current_view = f"Files: {', '.join(self.file_system.keys())}"
            reward = -0.01
        elif cmd == "READ_FILE":
            if target in self.file_system:
                self.current_view = self.file_system[target]
                reward = 0.1
            else: reward = -0.5
        elif cmd == "FLAG_BUG":
            if ":" not in target:
                self.system_msg = "Invalid format. Use file:BUG_TYPE"
                reward = -0.5
            elif target not in self.flagged_bugs:
                self.flagged_bugs.add(target)
                reward = 0.5
            else: reward = -0.1
        elif cmd == "SUBMIT_REVIEW":
            done = True
            correct = sum(1 for f, b in self.actual_bugs.items() if f"{f}:{b}" in self.flagged_bugs)
            false_pos = len(self.flagged_bugs) - correct
            reward = (correct * 5.0) - (false_pos * 3.0)
            if correct == len(self.actual_bugs) and false_pos == 0: reward += 10.0
        return self._get_obs(), reward, done