# OpenEnv Quantum Aladdin (Enterprise Trading AI)

## Environment Description & Motivation
This OpenEnv environment safely simulates real-world tasks required for the AI Trading Agents Hackathon. The environment and the native `aladdin_core.py` engine challenge traditional bot structures by deploying an **Enterprise-Grade "Aladdin-Killer" Architecture**.

The Quantum Aladdin Engine fuses:
- **Big Data Data-Lakes**: Telemetry ingestion from PRISM.
- **Vision AI**: Multi-dimensional thermal orderbook chart analysis.
- **Voice / NLP AI**: Sentiment scoring from macroeconomic audio transcripts.
- **ERC-8004 Trustless Intents**: Institutional action-logging to decentralized vaults.
- **Kraken CLI Integrations**: Native large-batch programmatic execution routing.

## Spaces Definition

### Action Space
- `code` (str): The exact Python/Pandas string that modifies the local `df` variable in place.

### Observation Space
- `df_head` (str): A string representation of the current `df.head()`.
- `columns` (List[str]): Current columns in the dataframe.
- `missing_counts` (dict): A dictionary pairing columns to their NaN count.
- `task_id` (int): The current underlying configuration target.

## Task Descriptions (Difficulty Range)

1. **Task 1 - Easy: Kraken CLI PnL Calculation**
   - Goal: Calculate 'net_pnl' by subtracting 'fees' from 'gross_pnl' in the Kraken CLI trading dataframe.
2. **Task 2 - Medium: ERC-8004 Reputation Formatting**
   - Goal: Fill missing values in the ERC-8004 'reputation_score' column with 0 for the identity registry.
3. **Task 3 - Hard: PRISM AI Signal Normalization**
   - Goal: Convert the 'signal' column to lowercase to normalize PRISM AI market signals.

## Setup and Usage Instructions

1. **Docker Deployment (for HF Spaces)**
   ```sh
   docker build -t openenv-quantum-cleaner .
   docker run -p 8000:8000 openenv-quantum-cleaner
   ```

2. **Running the Baseline Inference Script**
   Ensure your OPENAI compatible API URL and token are set if you are testing:
   ```sh
   export MODEL_NAME="gpt-4o-mini"
   export API_BASE_URL="https://api.openai.com/v1"
   export HF_TOKEN="your-api-key"
   python inference.py
   ```
