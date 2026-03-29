#!/usr/bin/env python3
"""Pretooluse hook with logging"""
import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Log file path
log_file = Path(__file__).parent / "hook.log"

def log(message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")

try:
    # Read input
    input_data = json.load(sys.stdin)
    log(f"Input: {json.dumps(input_data)}")

    # Extract tool info
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Check if this is a cppcheck tool
    if "cppcheck" not in tool_name:
        log("Not cppcheck, returning empty hook response")
        response = {"hookSpecificOutput": {"hookEventName": "PreToolUse"}}
        sys.stdout.write(json.dumps(response))
        sys.stdout.flush()
        sys.exit(0)

    target_path = tool_input.get("target_path", "")
    log(f"Target path: {target_path}")

    if not target_path or Path(target_path).is_absolute():
        log("Already absolute or empty, returning empty hook response")
        response = {"hookSpecificOutput": {"hookEventName": "PreToolUse"}}
        sys.stdout.write(json.dumps(response))
        sys.stdout.flush()
        sys.exit(0)

    cwd = input_data.get("cwd", os.getcwd())
    log(f"CWD: {cwd}")

    absolute_path = str((Path(cwd) / target_path).resolve())
    log(f"Converted to: {absolute_path}")

    # Modify tool_input
    tool_input["target_path"] = absolute_path

    # Return standard hook response with modified tool input
    response = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Normalize target_path to absolute path",
            "updatedInput": tool_input
        }
    }

    log(f"Response sent to Claude: {json.dumps(response)}")
    sys.stdout.write(json.dumps(response))
    sys.stdout.flush()

except Exception as e:
    log(f"Error: {e}")
    raise
