from datetime import datetime

logs = []

def log(message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    logs.append(f"{timestamp} {message}")
    print(f"{timestamp} {message}")

def get_logs():
    return logs[-100:]  # Return last 100 logs for performance
