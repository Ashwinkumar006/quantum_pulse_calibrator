import requests
import json

base = "http://127.0.0.1:7860"

print("=" * 60)
print("QUANTUM PULSE CALIBRATOR - PRE-SUBMISSION CHECK")
print("=" * 60)

# Test 1: Health Check GET /
r = requests.get(base + "/")
print(f"\n[1] GET /  => {r.status_code}")
print(f"    Response: {r.json()}")
assert r.status_code == 200, "FAILED: Health check down!"
print("    ✅ PASSED")

# Test 2: POST /reset task 1
r = requests.post(base + "/reset", json={"task_id": 1})
print(f"\n[2] POST /reset task_id=1 => {r.status_code}")
data = r.json()
obs = data.get("observation", data)
print(f"    Columns: {obs['columns']}")
assert "kraken_trade_id" in obs["columns"], "FAILED: Wrong task 1 data!"
print("    ✅ PASSED")

# Test 3: POST /step with correct code
code = "df['net_pnl'] = df['gross_pnl'] - df['fees']"
r2 = requests.post(base + "/step", json={"code": code})
print(f"\n[3] POST /step (task 1 grader) => {r2.status_code}")
step_data = r2.json()
reward = step_data["reward"]["value"]
print(f"    Reward: {reward} | Done: {step_data['done']}")
assert reward == 1.0, f"FAILED: Expected reward=1.0, got {reward}"
print("    ✅ PASSED - Reward=1.0!")

# Test 4: POST /reset task 2
r = requests.post(base + "/reset", json={"task_id": 2})
print(f"\n[4] POST /reset task_id=2 => {r.status_code}")
obs = r.json().get("observation", r.json())
assert "reputation_score" in obs["columns"], "FAILED: Wrong task 2 data!"
print("    ✅ PASSED")

# Test 5: POST /step task 2
code2 = "df['reputation_score'] = df['reputation_score'].fillna(0)"
r2 = requests.post(base + "/step", json={"code": code2})
print(f"\n[5] POST /step (task 2 grader) => {r2.status_code}")
reward2 = r2.json()["reward"]["value"]
print(f"    Reward: {reward2}")
assert reward2 == 1.0, f"FAILED: Expected reward=1.0, got {reward2}"
print("    ✅ PASSED - Reward=1.0!")

# Test 6: POST /reset task 3
r = requests.post(base + "/reset", json={"task_id": 3})
print(f"\n[6] POST /reset task_id=3 => {r.status_code}")
obs = r.json().get("observation", r.json())
assert "signal" in obs["columns"], "FAILED: Wrong task 3 data!"
print("    ✅ PASSED")

# Test 7: POST /step task 3
code3 = "df['signal'] = df['signal'].str.lower()"
r2 = requests.post(base + "/step", json={"code": code3})
print(f"\n[7] POST /step (task 3 grader) => {r2.status_code}")
reward3 = r2.json()["reward"]["value"]
print(f"    Reward: {reward3}")
assert reward3 == 1.0, f"FAILED: Expected reward=1.0, got {reward3}"
print("    ✅ PASSED - Reward=1.0!")

print("\n" + "=" * 60)
print("✅ ALL 7 CHECKS PASSED. READY FOR SUBMISSION.")
print("=" * 60)
