import json
import os
from datetime import datetime, timedelta

LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def log_user_action(user_id, username, action, data=None, result=None):
    try:
        log_file = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.json")
        
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id,
            "username": username or "Unknown",
            "action": action,
            "data": data or {},
            "result": result or "Success"
        }
        
        existing_logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                existing_logs = json.load(f)
        
        existing_logs.append(log_entry)
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(existing_logs, f, indent=2, ensure_ascii=False)
            
        return True
    except Exception as e:
        print(f"Logging error: {e}")
        return False

def get_user_logs(user_id=None, days=7):
    try:
        all_logs = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            log_file = os.path.join(LOG_DIR, f"{date}.json")
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    if user_id:
                        logs = [l for l in logs if l.get('user_id') == user_id]
                    all_logs.extend(logs)
        return all_logs
    except Exception as e:
        return []

def get_all_logs_since(days=7):
    return get_user_logs(user_id=None, days=days)