import os
import json

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

DEFAULT_CONFIG = {
    "active_target": "ALL ACCOUNTS",
    "accounts": [],
    "favorites": [],
    "visibility_filter": "ALL"
}

def _ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def load_config():
    _ensure_data_dir()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                # Ensure all key structures exist
                for key, val in DEFAULT_CONFIG.items():
                    if key not in data:
                        data[key] = val
                return data
        except Exception:
            return DEFAULT_CONFIG.copy()
    
    # Check for legacy files to migrate
    config = DEFAULT_CONFIG.copy()
    legacy_accounts = os.path.join(DATA_DIR, "accounts.json")
    if os.path.exists(legacy_accounts):
        try:
            with open(legacy_accounts, "r") as f:
                config["accounts"] = json.load(f)
        except Exception:
            pass
            
    save_config(config)
    return config

def save_config(config):
    _ensure_data_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def get_accounts():
    return load_config().get("accounts", [])

def add_account(username, password):
    cfg = load_config()
    for acc in cfg["accounts"]:
        if acc["username"].lower() == username.lower():
            acc["password"] = password
            acc["status"] = "Active"
            save_config(cfg)
            return
    cfg["accounts"].append({
        "username": username,
        "password": password,
        "status": "Active"
    })
    save_config(cfg)

def get_active_target():
    return load_config().get("active_target", "ALL ACCOUNTS")

def set_active_target(target):
    cfg = load_config()
    cfg["active_target"] = target
    save_config(cfg)

def get_favorites():
    return load_config().get("favorites", [])

def is_favorite(username):
    favs = get_favorites()
    return any(f["username"].lower() == username.lower() for f in favs)

def mark_favorite(profile_data):
    cfg = load_config()
    username = profile_data.get("username", "").lower()
    if not is_favorite(username):
        cfg["favorites"].append(profile_data)
        save_config(cfg)
        return True
    return False

def unmark_favorite(username):
    cfg = load_config()
    orig_len = len(cfg["favorites"])
    cfg["favorites"] = [f for f in cfg["favorites"] if f.get("username", "").lower() != username.lower()]
    if len(cfg["favorites"]) < orig_len:
        save_config(cfg)
        return True
    return False

def get_visibility_filter():
    return load_config().get("visibility_filter", "ALL")

def set_visibility_filter(mode):
    cfg = load_config()
    cfg["visibility_filter"] = mode
    save_config(cfg)
