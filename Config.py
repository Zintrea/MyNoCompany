import autogen
import sys
import re
import os
from dotenv import load_dotenv

load_dotenv()

def _get_api_keys():
    keys = []
    for i in range(1, 10):
        key = os.getenv(f"DEEPSEEK_API_KEY_{i}")
        if key and not key.startswith("YOUR_"):
            keys.append(key)
    return keys

# =================================================================
# DeepSeek Model Priority List
# =================================================================

MODEL_PRIORITY_LIST = [
    "deepseek-chat",
    "deepseek-coder",
]

# =================================================================
# API Keys & Looping Config List
# =================================================================

API_KEYS = _get_api_keys()

DEEPSEEK_BASE_URL = "https://api.deepseek.com"

def get_fallback_config_list():
    config_list = []
    
    for _ in range(50):
        for model in MODEL_PRIORITY_LIST:
            for key in API_KEYS:
                config_list.append({
                    "model": model,
                    "api_key": key,
                    "api_type": "openai",
                    "base_url": DEEPSEEK_BASE_URL,
                })
    return config_list

fallback_config_list = get_fallback_config_list()

# =================================================================
# Logger System
# =================================================================
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("meeting_log.txt", "a", encoding="utf-8")

    def write(self, message):
        try:
            self.terminal.write(message)
        except UnicodeEncodeError:
            clean_for_terminal = message.encode('ascii', 'replace').decode('ascii')
            self.terminal.write(clean_for_terminal)
        
        clean_message = re.sub(r'\x1b\[[0-9;]*m', '', message) 
        self.log.write(clean_message)  
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

def start_logging():
    sys.stdout = Logger()
    print("[RED] System Logging Started: meeting_log.txt")

# =================================================================
# Export Configurations
# =================================================================

config_research = {
    "config_list": fallback_config_list,
    "temperature": 0.3,
    "max_tokens": 1500,
}

config_editor = {
    "config_list": fallback_config_list,
    "temperature": 0.7,
    "max_tokens": 2000,
}

config_writer = {
    "config_list": fallback_config_list,
    "temperature": 0.9,
    "max_tokens": 4096,
}
