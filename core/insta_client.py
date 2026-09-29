import os
import json
from instagrapi import Client
from core.account_manager import get_active_target, load_accounts
from rich.console import Console

console = Console()
_client_instance = None

def get_client():
    global _client_instance
    if _client_instance is not None:
        return _client_instance
        
    active = get_active_target()
    accounts = load_accounts()
    
    password = None
    for acc in accounts:
        if acc['username'] == active:
            password = acc['password']
            break
            
    if not password:
        console.print("[bold red]Failed to find password for active account in config.[/bold red]")
        return None
        
    client = Client()
    
    # Setup session loading to avoid bans
    session_file = f"data/{active}_session.json"
    
    try:
        console.print(f"[bold grey74]Connecting to Instagram as @{active}...[/bold grey74]")
        if os.path.exists(session_file):
            client.load_settings(session_file)
            client.login(active, password)
            client.get_timeline_feed() # verify session
        else:
            client.login(active, password)
            client.dump_settings(session_file)
            
        console.print(f"[bold green]✔ Successfully connected to Instagram API as @{active}[/bold green]")
        _client_instance = client
        return _client_instance
    except Exception as e:
        console.print(f"[bold red]Instagram Login Failed: {e}[/bold red]")
        return None
