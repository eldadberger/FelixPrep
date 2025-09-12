from typing import Any, Dict


def replace_id_recursive(obj: Any) -> Any:
    """
    Recursively replace '_id' keys with 'id' in dicts/lists.
    """
    if isinstance(obj, dict):
        new_dict: Dict[str, Any] = {}
        for k, v in obj.items():
            new_key = "id" if k == "_id" else k
            new_dict[new_key] = replace_id_recursive(v)
        return new_dict
    elif isinstance(obj, list):
        return [replace_id_recursive(i) for i in obj]
    return obj
