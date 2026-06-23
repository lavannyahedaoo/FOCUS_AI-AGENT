import json
import logging
import time
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/execution.log",
    level=logging.INFO,
    format="%(message)s"
)

def log_event(agent: str, action: str, trace_id: str, payload: dict, tokens_used: int = 0):
    log_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "agent": agent,
        "action": action,
        "trace_id": trace_id,
        "payload": payload,
        "tokens_used": tokens_used
    }
    logging.info(json.dumps(log_data))
