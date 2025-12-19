# Response при создании команды
CREATE_COMMAND_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "status": {"type": "string", "enum": ["NEW"]}
    },
    "required": ["id", "status"],
    "additionalProperties": False
}

# Response при получении статуса
COMMAND_STATUS_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "status": {"type": "string", "enum": ["NEW", "IN_PROGRESS", "SUCCESS", "FAILED"]},
        "result": {"type": "string"}
    },
    "required": ["id", "status"],
    "additionalProperties": False
}