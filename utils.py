import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "chat_log.txt")

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("JSON Load Error:", e)
        return {}

def log_chat(user_input, response):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] User: {user_input}\n")
            f.write(f"[{timestamp}] Bot: {response}\n")
            f.write("-" * 50 + "\n")
    except Exception as e:
        print("Logging Error:", e)
    