import os
import json
from rich.console import Console

console = Console()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

def _ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def load_config():
    _ensure_data_dir()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {"accounts": [], "active_target": "ALL ACCOUNTS"}
    return {"accounts": [], "active_target": "ALL ACCOUNTS"}

def save_config(config):
    _ensure_data_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def load_accounts():
    config = load_config()
    return config.get("accounts", [])

def save_accounts(accounts):
    config = load_config()
    config["accounts"] = accounts
    save_config(config)

def add_account(username, password):
    config = load_config()
    accounts = config.get("accounts", [])
    
    # Check if account already exists
    for acc in accounts:
        if acc["username"].lower() == username.lower():
            acc["password"] = password
            acc["status"] = "Active"
            save_accounts(accounts)
            return
            
    accounts.append({
        "username": username,
        "password": password,
        "status": "Active"
    })
    config["accounts"] = accounts
    save_config(config)

def get_active_target(*args, **kwargs):
    config = load_config()
    return config.get("active_target", "ALL ACCOUNTS")

def set_active_target(target_name):
    config = load_config()
    config["active_target"] = target_name
    save_config(config)

def get_favorites():
    config = load_config()
    return config.get("favorites", [])

def add_favorite(profile_data):
    config = load_config()
    favorites = config.get("favorites", [])
    
    # Avoid duplicates by username
    if not any(f.get("username") == profile_data.get("username") for f in favorites):
        favorites.append(profile_data)
        config["favorites"] = favorites
        save_config(config)
        return True
    return False

def get_chatted_users():
    config = load_config()
    return config.get("chatted_users", [])

def add_chatted_user(username):
    config = load_config()
    chatted = config.get("chatted_users", [])
    
    if username not in chatted:
        chatted.append(username)
        config["chatted_users"] = chatted
        save_config(config)
        return True
    return False

def get_following():
    config = load_config()
    return config.get("following", [])

def add_following(username):
    config = load_config()
    following = config.get("following", [])
    if username not in following:
        following.append(username)
        config["following"] = following
        save_config(config)
        return True
    return False
