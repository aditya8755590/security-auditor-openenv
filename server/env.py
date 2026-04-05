from server.models import Observation, Action
class SecurityEnv:
    def __init__(self):
        # Simulated File System (The GitHub Pull Request)
        self.file_system = {
            "main.py": """
import os
from auth import login
from utils import process_data

if __name__ == "__main__":
    user = input("Enter username: ")
    pwd = input("Enter password: ")
    if login(user, pwd):
        print("Welcome!")
    process_data()
""",
            "auth.py": """
def login(user, pwd):
    dummy_password = 'test_password_123'  # TODO: remove before prod
    
    if user == "admin":
        return True   # 🔥 AUTH BYPASS BUG
    
    return pwd == dummy_password
""",
            "db.py": """
def get_user(email):
    query = "SELECT * FROM users WHERE email = '" + email + "'"
    cursor.execute(query)
""",
            "settings.py": """
import os
api_key = os.getenv('STRIPE_API_KEY')

if not api_key:
    api_key = "sk_test_123456"  # 🔥 FALLBACK SECRET
""",
            "worker.py": """
def process_jobs(queue):
    while True:   # 🔥 Infinite loop
        if len(queue) == 0:
            continue
        job = queue.pop(0)
        print("Processing", job)
""",
            "leak.cpp": """
#include <vector>
using namespace std;

void leak() {
    vector<int*> arr;
    while(true) {
        int* x = new int(10);  // 🔥 memory leak
        arr.push_back(x);
    }
}
""",
            "utils.py": """
import pickle

def process_data():
    data = input("Enter data: ")
    obj = pickle.loads(data)   # 🔥 RCE risk
    print(obj)
""",
            "deploy.py": """
import os

def deploy(branch):
    os.system("git checkout " + branch)  # 🔥 command injection
"""
        }
        
        # The Ground Truth (What the agent SHOULD find)
        self.actual_bugs = {
            "db.py": "SQL_INJECTION",
            "auth.py": "AUTH_BYPASS",
            "settings.py": "HARDCODED_SECRET",
            "worker.py": "INFINITE_LOOP",
            "leak.cpp": "MEMORY_LEAK",
            "utils.py": "UNSAFE_DESERIALIZATION",
            "deploy.py": "COMMAND_INJECTION"
        }
        
        # State tracking variables
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
            current_directory="root",
            available_files=list(self.file_system.keys()),
            file_content_view=self.current_view,
            bugs_flagged_count=len(self.flagged_bugs),
            system_message=self.system_msg
        )

    def step(self, action: Action):
        reward = 0.0
        done = False
        
        cmd = action.command
        target = action.target
        
        if cmd == "LIST_FILES":
            self.current_view = f"Files: {', '.join(self.file_system.keys())}"
            self.system_msg = "Listed files."
            reward = -0.01 
            
        elif cmd == "READ_FILE":
            if target in self.file_system:
                self.current_view = self.file_system[target]
                self.system_msg = f"Opened {target}"
                reward = 0.1 
            else:
                self.system_msg = "Error: File not found."
                reward = -0.5 
                
        elif cmd == "FLAG_BUG":
            # Upgraded: Strict format validation
            if ":" not in target:
                self.system_msg = "Invalid format. Use file:BUG_TYPE"
                reward = -0.5
            elif target not in self.flagged_bugs:
                self.flagged_bugs.add(target)
                self.system_msg = f"Flagged bug: {target}"
                reward = 0.5
            else:
                self.system_msg = "Bug already flagged."
                reward = -0.1
                
        elif cmd == "SUBMIT_REVIEW":
            done = True
            self.system_msg = "Review submitted."
            
            correct_flags = 0
            for file, bug_type in self.actual_bugs.items():
                expected_target = f"{file}:{bug_type}"
                if expected_target in self.flagged_bugs:
                    correct_flags += 1
                    
            false_positives = len(self.flagged_bugs) - correct_flags
            
            # Upgraded: Brutal penalty for false positives
            reward = (correct_flags * 5.0) - (false_positives * 3.0)
            
            if correct_flags == len(self.actual_bugs) and false_positives == 0:
                reward += 10.0 
                
        else:
            self.system_msg = "Error: Invalid command."
            reward = -0.5
            
        return self._get_obs(), reward, done