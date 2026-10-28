"""In-memory pending actions store for confirmation workflows."""
import uuid
from typing import Any, Dict, Optional

_pending_actions: Dict[str, Dict[str, Any]] = {}

def create_pending_action(action_type: str, data: Dict[str, Any]) -> str:
    """Save pending action data and return unique action id."""
    action_id = str(uuid.uuid4())[:8]
    _pending_actions[action_id] = {
        "type": action_type,
        "data": data
    }
    return action_id

def get_pending_action(action_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve pending action by id."""
    return _pending_actions.get(action_id)

def pop_pending_action(action_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve and delete pending action by id."""
    return _pending_actions.pop(action_id, None)
