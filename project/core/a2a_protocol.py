import time
import uuid

def create_a2a_message(sender: str, recipient: str, trace_id: str, command: str, payload: dict) -> dict:
    return {
        "message_id": f"msg_{uuid.uuid4().hex[:8]}",
        "trace_id": trace_id,
        "sender": sender,
        "recipient": recipient,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "payload": {
            "command": command,
            **payload
        }
    }

def validate_a2a_message(message: dict) -> bool:
    required_keys = {"message_id", "trace_id", "sender", "recipient", "timestamp", "payload"}
    return required_keys.issubset(message.keys())
