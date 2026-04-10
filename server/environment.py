from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np

# --- OpenEnv Spec Models ---
class Action(BaseModel):
    code: str  # The python code to execute on the dataframe

class Observation(BaseModel):
    df_head: str
    columns: List[str]
    missing_counts: dict
    task_id: int

class Reward(BaseModel):
    value: float
    reason: str

# --- Environment Class ---
class EnvironmentState:
    def __init__(self):
        self.tasks = [
            {"id": "kraken_pnl_calc", "desc": "Calculate 'net_pnl' by subtracting 'fees' from 'gross_pnl' in the Kraken CLI trading dataframe.", "difficulty": "easy"},
            {"id": "erc8004_reputation", "desc": "Fill missing values in the ERC-8004 'reputation_score' column with 0.", "difficulty": "medium"},
            {"id": "prism_signal_normalization", "desc": "Convert 'signal' column to lowercase to normalize PRISM AI market signals.", "difficulty": "hard"}
        ]
        self.current_task_idx = 0
        self.df = None

    def reset(self, task_idx=1) -> Observation:
        # Convert 1-indexed (from spec) to 0-indexed local
        self.current_task_idx = max(0, task_idx - 1) 
        
        if self.current_task_idx == 0:
            self.df = pd.DataFrame({'kraken_trade_id': ['T1', 'T2', 'T3'], 'gross_pnl': [100.5, -20.0, 50.0], 'fees': [0.5, 0.1, 0.25]})
        elif self.current_task_idx == 1:
            self.df = pd.DataFrame({'agent_address': ['0x1A', '0x2B', '0x3C'], 'reputation_score': [85.0, np.nan, 92.5]})
        else:
            self.df = pd.DataFrame({'asset': ['BTC', 'ETH', 'SOL'], 'signal': ['BUY', 'Hold', 'sell']})
            
        return self._get_obs()

    def _get_obs(self) -> Observation:
        return Observation(
            df_head=self.df.head().to_string(),
            columns=list(self.df.columns),
            missing_counts=self.df.isnull().sum().to_dict(),
            task_id=self.current_task_idx + 1
        )

    def step(self, action: Action) -> tuple[Observation, Reward, bool, dict]:
        try:
            # Execute the code provided by the agent safely on the local df
            local_vars = {'df': self.df.copy()}
            exec(action.code, {}, local_vars)
            new_df = local_vars['df']
            
            # Grader Logic
            reward = self._grade(new_df)
            self.df = new_df
            return self._get_obs(), reward, True, {"reason": reward.reason, "success": reward.value > 0}
        except Exception as e:
            return self._get_obs(), Reward(value=0.01, reason=str(e)), True, {"error": str(e), "success": False}

    def _grade(self, df) -> Reward:
        if self.current_task_idx == 0:
            if 'net_pnl' in df.columns and (df['net_pnl'] == df['gross_pnl'] - df['fees']).all():
                return Reward(value=0.99, reason="Success")
        elif self.current_task_idx == 1:
            if not df['reputation_score'].isnull().any() and (df['reputation_score'].iloc[1] == 0.0):
                return Reward(value=0.99, reason="Success")
        elif self.current_task_idx == 2:
            if df['signal'].apply(lambda x: getattr(x, 'islower', lambda: False)()).all() or df['signal'].apply(lambda x: x == x.lower()).all() or df['signal'].str.islower().all():
                return Reward(value=0.99, reason="Success")
                
        return Reward(value=0.01, reason="Task criteria not met")

    def state(self) -> dict:
        return {
            "task_id": self.current_task_idx + 1,
            "columns": list(self.df.columns) if self.df is not None else []
        }
