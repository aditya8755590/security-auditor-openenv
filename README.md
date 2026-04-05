---
title: Security Auditor OpenEnv
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

# 🛡️ Security Code Auditor (Multi-Step RL Environment)

## 📖 Overview
This environment simulates a real-world **Senior Security Engineer's workflow**. Instead of basic line-by-line classification, this environment requires an AI agent to navigate a simulated file system (like a GitHub Pull Request), open specific files, identify vulnerabilities, and submit a final review. 

## 🧠 Multi-Step Decision Making
This environment tests an LLM's ability to plan, explore, and retain context over multiple steps, acting as a state machine.

### 🔍 Observation Space (What the Agent Sees)
*   `current_directory`: The agent's current location in the repository.
*   `available_files`: List of files in the current PR.
*   `file_content_view`: The code inside the currently opened file.
*   `bugs_flagged_count`: Track progress of identified vulnerabilities.
*   `system_message`: Feedback from the environment (e.g., "Opened db.py", "Error: File not found").

### 🕹️ Action Space (What the Agent Can Do)
The agent must issue specific commands to explore the environment:
1.  `LIST_FILES` - View the directory contents.
2.  `READ_FILE` (target = filename) - Open and read a file's code.
3.  `FLAG_BUG` (target = filename:bug_type) - Report a vulnerability (e.g., `db.py:SQL_INJECTION`).
4.  `SUBMIT_REVIEW` - Complete the audit and calculate the final score.

## 🏆 Reward Logic
*   **+0.1**: Exploring the codebase (opening real files).
*   **-0.5**: Hallucinating files or using invalid commands.
*   **+5.0**: Correctly identifying a real vulnerability.
*   **-2.0**: False positive penalty (flagging safe code).
*   **+10.0**: Perfect Run Bonus (Finding all bugs with zero false positives).

## 🚀 API Endpoints
*   `POST /reset`: Initializes the PR environment.
*   `POST /step`: Takes an action and returns the new state and reward.
*   `GET /state`: Health check endpoint.