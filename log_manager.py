from typing import List

logs: List[str] = []

def log(message: str):
    print(message)
    logs.append(message)
    if len(logs) > 1000:
        logs.pop(0)

def get_logs():
    return logs
