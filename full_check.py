"""
COMPLETE PRE-SUBMISSION CHECKLIST VALIDATOR
Checks every single item from the Scaler/Meta hackathon checklist.
"""
import os
import sys
import time
import requests
import subprocess
import json

base = "http://127.0.0.1:7860"
PASS = "[PASS]"
FAIL = "[FAIL]"
results = []

def check(name, passed, detail=""):
    status = PASS if passed else FAIL
    msg = f"{status} {name}"
    if detail:
        msg += f"\n       -> {detail}"
    print(msg)
    results.append((name, passed))
    return passed

print("=" * 65)
print("  FULL PRE-SUBMISSION CHECKLIST - QUANTUM PULSE CALIBRATOR")
print("=" * 65)

# -----------------------------------------------
# 1. FILES AT REPO ROOT
# -----------------------------------------------
print("\n-- FILE STRUCTURE --")
root = "H:\\ashwin\\ashwin\\meta"
check("inference.py at repo root", os.path.exists(os.path.join(root, "inference.py")))
check("app.py at repo root", os.path.exists(os.path.join(root, "app.py")))
check("environment.py at repo root", os.path.exists(os.path.join(root, "environment.py")))
check("Dockerfile at repo root", os.path.exists(os.path.join(root, "Dockerfile")))
check("openenv.yaml at repo root", os.path.exists(os.path.join(root, "openenv.yaml")))
check("requirements.txt at repo root", os.path.exists(os.path.join(root, "requirements.txt")))
check("README.md at repo root", os.path.exists(os.path.join(root, "README.md")))

# -----------------------------------------------
# 2. DOCKERFILE CONTENT CHECK
# -----------------------------------------------
print("\n-- DOCKERFILE CHECK --")
with open(os.path.join(root, "Dockerfile")) as f:
    df_content = f.read()
check("Dockerfile exposes port 7860", "7860" in df_content, "HuggingFace requires port 7860")
check("Dockerfile uses python:3.10", "python:3.10" in df_content)
check("Dockerfile runs uvicorn", "uvicorn" in df_content)

# -----------------------------------------------
# 3. README.md SDK CONFIG
# -----------------------------------------------
print("\n-- README.md HF CONFIG --")
with open(os.path.join(root, "README.md")) as f:
    rm_content = f.read()
check("README has sdk: docker", "sdk: docker" in rm_content, "Prevents infinite build loop on HF")
check("README has app_port: 7860", "app_port: 7860" in rm_content)

# -----------------------------------------------
# 4. MANDATORY ENV VARIABLES IN inference.py
# -----------------------------------------------
print("\n-- MANDATORY VARIABLES CHECK --")
with open(os.path.join(root, "inference.py")) as f:
    inf_content = f.read()
check("API_BASE_URL defined in inference.py", "API_BASE_URL" in inf_content)
check("MODEL_NAME defined in inference.py", "MODEL_NAME" in inf_content)
check("HF_TOKEN defined in inference.py", "HF_TOKEN" in inf_content)
check("OpenAI client used", "from openai import OpenAI" in inf_content)
check("[START] log format present", "[START]" in inf_content)
check("[STEP] log format present", "[STEP]" in inf_content)
check("[END] log format present", "[END]" in inf_content)

# -----------------------------------------------
# 5. openenv.yaml - 3+ TASKS CHECK
# -----------------------------------------------
print("\n-- OPENENV.yaml CHECK --")
with open(os.path.join(root, "openenv.yaml")) as f:
    yaml_content = f.read()
task_count = yaml_content.count("- id:")
check("openenv.yaml has 3+ tasks", task_count >= 3, f"Found {task_count} tasks")

# -----------------------------------------------
# 6. LIVE API ENDPOINT TESTS
# -----------------------------------------------
print("\n-- LIVE API TESTS (port 7860) --")
try:
    r = requests.get(base + "/", timeout=5)
    check("GET / returns 200", r.status_code == 200, str(r.json()))
except Exception as e:
    check("GET / returns 200", False, f"Server not running: {e}")
    print("\n[FATAL] Start the server first: uvicorn app:app --port 7860")
    sys.exit(1)

# Test all 3 tasks
tasks_data = [
    (1, "kraken_trade_id", "df['net_pnl'] = df['gross_pnl'] - df['fees']"),
    (2, "reputation_score", "df['reputation_score'] = df['reputation_score'].fillna(0)"),
    (3, "signal", "df['signal'] = df['signal'].str.lower()"),
]

for task_id, expected_col, solution_code in tasks_data:
    # reset
    r = requests.post(base + "/reset", json={"task_id": task_id}, timeout=5)
    check(f"POST /reset task_id={task_id} returns 200", r.status_code == 200)
    obs = r.json().get("observation", r.json())
    check(f"Task {task_id} dataframe has correct columns", expected_col in obs["columns"],
          f"Columns: {obs['columns']}")
    check(f"Task {task_id} missing_counts present", "missing_counts" in obs)
    check(f"Task {task_id} task_id in obs", obs.get("task_id") == task_id)

    # step with correct solution
    r2 = requests.post(base + "/step", json={"code": solution_code}, timeout=5)
    check(f"POST /step task_id={task_id} returns 200", r2.status_code == 200)
    step_data = r2.json()
    reward = step_data["reward"]["value"]
    check(f"Task {task_id} grader reward = 1.0", reward == 1.0, f"Got reward={reward}")
    check(f"Task {task_id} reward in [0.0, 1.0]", 0.0 <= reward <= 1.0)
    check(f"Task {task_id} done=True", step_data["done"] == True)

# state endpoint
r = requests.post(base + "/state", timeout=5)
check("POST /state returns 200", r.status_code == 200, str(r.json()))

# -----------------------------------------------
print("\n" + "=" * 65)
passed = sum(1 for _, p in results if p)
total = len(results)
failed = [(n, p) for n, p in results if not p]
print(f"  RESULT: {passed}/{total} checks passed")
if failed:
    print(f"\n  FAILED ITEMS:")
    for name, _ in failed:
        print(f"  [X] {name}")
    print("\n  [NOT READY] Fix the above issues before submitting!")
else:
    print("\n  ALL CHECKS PASSED - READY FOR SUBMISSION!")
print("=" * 65)
