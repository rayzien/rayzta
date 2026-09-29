import getpass
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from core.config_manager import add_account, get_accounts, set_active_target

console = Console()

def execute():
    console.clear()
    
    # Header panel
    console.print(Panel("[bold white]AUTHORIZER MODULE[/bold white]", style="bold red", expand=False))
    console.print("[bold grey74]Add and authenticate your Rayzta account credentials.[/bold grey74]\n")
    
    existing_accounts = get_accounts()
    if existing_accounts:
        console.print("[bold white]Currently Registered Accounts:[/bold white]")
        for idx, acc in enumerate(existing_accounts, 1):
            console.print(f"  [bold red][{idx}][/bold red] [bold white]@{acc['username']}[/bold white] ([grey74]{acc['status']}[/grey74])")
        console.print()

    username = console.input("[bold red]>[/bold red] [bold white]Enter Username to Add/Update:[/bold white] ").strip()
    if not username:
        console.print("[bold red]Username cannot be empty.[/bold red]")
        time.sleep(1)
        return

    password = getpass.getpass("\033[1;31m>\033[0m \033[1;37mEnter Password:\033[0m ")
    if not password:
        console.print("[bold red]Password cannot be empty.[/bold red]")
        time.sleep(1)
        return

    console.print()
    
    # Animation for auth
    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold red"),
        TextColumn("[bold grey74]Authenticating & Saving credentials for {task.description}...[/bold grey74]"),
        console=console,
        transient=True
    ) as progress:
        progress.add_task(description=f"[bold white]@{username}[/bold white]", total=None)
        time.sleep(1.8)
        
    add_account(username, password)
    
    console.print(f"[bold red]>[/bold red] [bold white]Authentication Successful![/bold white] [grey74]Saved @{username} to config.json[/grey74]")
    
    set_active = console.input("\n[bold red]>[/bold red] [bold white]Set @{username} as current Active Target? (y/N):[/bold white] ").strip().lower()
    if set_active == 'y':
        set_active_target(username)
        console.print(f"[bold red]>[/bold red] [bold white]Active target updated to @{username}[/bold white]")
        time.sleep(1)
    else:
        time.sleep(1)
