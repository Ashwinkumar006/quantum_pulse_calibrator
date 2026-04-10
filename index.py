import os
import sys
import time
import platform
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="[INDEX CORE] %(message)s")

# =========================================================================
# CROSS-PLATFORM SYSTEM INDEX ROUTER
# Redirecting to respective module directories natively.
# =========================================================================

CWD = os.getcwd()
SYS_OS = platform.system()

logging.info(f"Booting Native Index Router on {SYS_OS} Architecture...")

# ---------------------------------------------------------
# DIRECTORY REDIRECTION INTEGRATION
# Mapping AI, Database, Backend, Frontend, and Auth
# ---------------------------------------------------------

# 1. FRONTEND / SAAS REDIRECT
POCKETSFLOW_DIR = CWD
sys.path.append(POCKETSFLOW_DIR)
logging.info(f"-> [FRONTEND MAPPED] Redirecting UI protocols to natively loaded Pocketsflow scripts at: {POCKETSFLOW_DIR}")

# 2. BACKEND / GOCLAW REDIRECT
BACKEND_DIR = os.path.join(CWD, "goclaw")
sys.path.append(BACKEND_DIR)
logging.info(f"-> [BACKEND MAPPED] Redirecting concurrency logic to Go-Bindings at: {BACKEND_DIR}")

# 3. DATABASE / ERC-8004 REDIRECT
DATABASE_DIR = os.path.join(CWD, "dexter")
sys.path.append(DATABASE_DIR)
logging.info(f"-> [DATABASE MAPPED] Redirecting decentralized ledger execution to: {DATABASE_DIR}")

# 4. AI / ML / DL / VISION REDIRECT
AI_DIR = os.path.join(CWD, "agency-agents")
sys.path.append(AI_DIR)
logging.info(f"-> [AI/ML MAPPED] Redirecting Swarm Intelligence & Vision logic to: {AI_DIR}")

# 5. AUTHENTICATION / CYBERSECURITY REDIRECT
AUTH_DIR = os.path.join(CWD, "pentagi")
sys.path.append(AUTH_DIR)
logging.info(f"-> [AUTHENTICATION MAPPED] Redirecting PentaGI vulnerability scanning to: {AUTH_DIR}")

# ---------------------------------------------------------
# EXECUTION (Redirecting to the Master Module)
# ---------------------------------------------------------
if __name__ == "__main__":
    logging.info("\nALL DIRECTORIES INTERLINKED TO INDEX. REDIRECTING EXECUTION...")
    try:
        # We redirect flow execution directly to the central quantum processing file we built
        print("\n=======================================================")
        import omega_quantum_claw
        omega = omega_quantum_claw.OpenClawMaster()
        omega.omega_sequence()
        print("=======================================================\n")
        logging.info("Index Redirect and Sub-directory execution completely successful.")
    except Exception as e:
        logging.error(f"Execution Error during redirect: {e}")
