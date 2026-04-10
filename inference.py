import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Mandatory variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
HF_TOKEN = os.getenv("HF_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

# If testing locally
ENV_API_URL = os.getenv("ENV_API_URL", "http://127.0.0.1:7860")

client = OpenAI(
    api_key=OPENAI_API_KEY or HF_TOKEN or "dummy-key",
    base_url=API_BASE_URL
)

def run_task(task_id: int):
    # Mapping to your internal string IDs for the START log
    task_names = ["kraken_pnl_calc", "erc8004_reputation", "prism_signal_normalization"]
    task_name = task_names[task_id - 1]
    benchmark = "AITradingAgentsBench"
    
    print(f"[START] task={task_name} env={benchmark} model={MODEL_NAME}", flush=True)
    
    # 1. Reset Environment via HTTP API
    try:
        resp = requests.post(f"{ENV_API_URL}/reset", json={"task_id": task_id})
        resp.raise_for_status()
        obs_payload = resp.json()
        obs = obs_payload.get("observation", obs_payload)
    except Exception as e:
        print(f"Failed to reset environment: {e}")
        return

    # Extract dynamic task descriptions
    descriptions = [
        "Calculate 'net_pnl' by subtracting 'fees' from 'gross_pnl' in the Kraken CLI trading dataframe.",
        "Fill missing values in the ERC-8004 'reputation_score' column with 0.",
        "Convert 'signal' column to lowercase to normalize PRISM AI market signals."
    ]
    task_desc = descriptions[task_id - 1]

    # 2. Get LLM Response
    prompt = f"Given this quantum dataframe: {obs['df_head']}. Task: {task_desc}. Provide ONLY the python code modifying the variable 'df'."
    
    done = False
    step = 0
    success = False
    score = 0.01
    error_msg = "null"
    code = ""

    step += 1
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        message_content = response.choices[0].message.content
        code = message_content.strip() if message_content else ""
        
        # Strip markdown safely
        if '```' in code:
            lines = code.split('\n')
            code = '\n'.join([l for l in lines if not l.startswith('```')])
            
        # 3. Apply Action via HTTP API - send flat Action model directly
        step_payload = {"code": code}
        step_resp = requests.post(f"{ENV_API_URL}/step", json=step_payload)
        step_resp.raise_for_status()
        step_data = step_resp.json()
        
        reward = step_data["reward"]["value"]
        done = step_data["done"]
        info = step_data["info"]
        
        success = info.get("success", False)
        score = float(reward)  # Direct score mapping
        raw_err = info.get("error", None)
        error_msg = str(raw_err) if raw_err else "null"
        
        action_log = code.replace('\n', ' ; ').replace('"', "'")
        print(f"[STEP]  step={step} action=\"{action_log}\" reward={reward:.2f} done={str(done).lower()} error={error_msg}", flush=True)
        
    except Exception as e:
        error_msg = str(e).replace('"', "'")
        print(f"[STEP]  step={step} action=none reward=0.01 done=false error=\"{error_msg}\"", flush=True)

    print(f"[END]   success={str(success).lower()} steps={step} score={score:.2f} rewards={score:.2f}", flush=True)

if __name__ == "__main__":
    for task in [1, 2, 3]:
        run_task(task)
