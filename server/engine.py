import subprocess
import tempfile
import os

# 🎯 The 3 Real Tasks (Buggy Code + Hidden Unit Tests)
TASKS = {
    "Task_1_Easy": {
        "description": "Fix the Two Sum algorithm. It currently returns wrong indices.",
        "buggy_code": "def two_sum(nums, target):\n    for i in range(len(nums)):\n        for j in range(len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]\n    return []\n",
        "test_code": """
assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
assert two_sum([3, 3], 6) == [0, 1]
print("ALL_TESTS_PASSED")
"""
    },
    "Task_2_Medium": {
        "description": "Fix the Binary Search algorithm. It has an infinite loop bug.",
        "buggy_code": "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low < high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid\n        else:\n            high = mid - 1\n    return -1\n",
        "test_code": """
assert binary_search([-1,0,3,5,9,12], 9) == 4
assert binary_search([-1,0,3,5,9,12], 2) == -1
print("ALL_TESTS_PASSED")
"""
    },
    "Task_3_Hard": {
        "description": "Fix the JSON parser bug. It fails on nested empty dictionaries.",
        "buggy_code": "def parse_custom(data):\n    if not data:\n        return None\n    return {k: parse_custom(v) if isinstance(v, dict) else v for k, v in data.items()}\n",
        "test_code": """
assert parse_custom({"a": 1}) == {"a": 1}
assert parse_custom({"a": {}}) == {"a": {}}
print("ALL_TESTS_PASSED")
"""
    }
}

class CodeExecutor:
    @staticmethod
    def run_tests(agent_code: str, test_code: str) -> dict:
        """Runs the agent's patched code + hidden tests in a real subprocess."""
        combined_code = agent_code + "\n" + test_code
        
        # Write to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(combined_code)
            temp_filepath = temp_file.name

        try:
            # Execute the file safely with a 3-second timeout
            result = subprocess.run(
                ["python", temp_filepath],
                capture_output=True,
                text=True,
                timeout=3
            )
            
            output = result.stdout + result.stderr
            passed = "ALL_TESTS_PASSED" in output
            
            return {
                "success": passed,
                "output": output.strip(),
                "error": None if result.returncode == 0 else "Execution Failed"
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "output": "Timeout: Code took too long to run (Infinite Loop?).", "error": "Timeout"}
        finally:
            os.remove(temp_filepath) # Cleanup