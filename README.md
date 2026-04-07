# 🛡️ Security Auditor OpenEnv

An advanced, multi-step Reinforcement Learning (RL) environment built on the OpenEnv spec. This system simulates a stateful backend file system, allowing LLM agents to act as Security Engineers and autonomously audit code for vulnerabilities.

## 🚀 Overview

The **Security Auditor** environment forces AI agents to move beyond simple Q&A and execute a "Real-World Task Simulation." The agent must navigate a simulated file system, read application code, identify specific security vulnerabilities, and submit a final audit report. 

This environment is fully compliant with the Meta OpenEnv specification, featuring strict Pydantic typing, multi-mode deployment capabilities (Local, Docker, Hugging Face), and deterministic programmatic graders.

## 🎯 The Three Tasks

The environment evaluates agents across an escalating difficulty curve. Each task has a deterministic grader that scores performance strictly between `0.0` and `1.0`.

1. **Task 1: Dependency Audit (Easy)**
   - **Objective:** The agent must locate package configuration files (`requirements.txt`, `package.json`) and flag known vulnerable or outdated dependencies.
2. **Task 2: Authentication Audit (Medium)**
   - **Objective:** The agent must navigate to middleware/authentication files, read the implementation, and flag insecure token handling or missing authorization scopes.
3. **Task 3: Data Leak / Deserialization (Hard)**
   - **Objective:** The agent must trace data flow across multiple files (e.g., from an API route to a utility function) to identify an unsafe deserialization or SQL injection vulnerability.

## 🛠️ System Architecture & Mechanics

- **Stateful Virtual File System:** The environment maintains a persistent state across steps. Actions like `READ_FILE` dynamically update the agent's observation space with realistic console outputs and file contents.
- **Action Space:** Agents interact using structured commands: `LIST_FILES`, `READ_FILE`, `FLAG_VULNERABILITY`, and `SUBMIT_REPORT`.
- **Meaningful Reward Shaping:** - `+0.1` for exploratory progress (reading relevant files).
  - `+0.5` for correctly identifying a bug location.
  - `-0.1` for invalid commands or hallucinated file paths.
  - `-1.0` (Terminal) for submitting a report with false positives.
- **Sandboxed Execution:** Vulnerabilities are simulated via text strings and mock states, ensuring the host server is never exposed to actual malicious code execution.

## 💻 Tech Stack

- **Backend:** FastAPI, Python 3.10+
- **RL Framework:** OpenEnv Core
- **Validation:** Pydantic
- **Packaging:** `uv`, `pyproject.toml`
- **Deployment:** Docker, Hugging Face Spaces

## 🏁 Getting Started

### Multi-Mode Deployment

**1. Run Locally (Standard)**
```bash
pip install uv
uv sync
uv run uvicorn server.app:app --host 0.0.0.0 --port 7860