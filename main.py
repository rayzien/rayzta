import os
import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
import pyfiglet

from core.plugin_loader import load_plugins
from core.account_manager import load_accounts, get_active_target, set_active_target

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    # Generate Slanted ASCII Art for Rayzta
    f = pyfiglet.Figlet(font='slant')
    ascii_art = f.renderText('R A Y Z T A')
    
    # Stylize banner with strict Red/White/Grey palette
    console.print(f"[bold red]{ascii_art}[/bold red]")
    console.print("[bold grey74]=======================================================[/bold grey74]")
    console.print("[bold white]   700X STRONGER AUTOMATION [/bold white] | [bold red]PLUG & PLAY ENGINE[/bold red]")
    console.print("[bold grey74]=======================================================[/bold grey74]\n")

def startup_sequence():
    clear_screen()
    with Progress(
        SpinnerColumn(spinner_name="line", style="bold red"),
        TextColumn("[bold grey74]{task.description}[/bold grey74]"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Initializing Rayzta Core...", total=None)
        time.sleep(0.6)
        progress.update(task, description="Loading Plugin Architecture...")
        time.sleep(0.6)
        progress.update(task, description="Mounting Account Manager...")
        time.sleep(0.4)

def account_selector_menu():
    while True:
        print_banner()
        accounts = load_accounts()
        current_target = get_active_target()
        
        console.print(Panel("[bold white]ACCOUNT MANAGER & TARGET SELECTOR[/bold white]", style="bold red", expand=False))
        console.print(f"[bold grey74]Current Active Target:[/bold grey74] [bold red]{current_target}[/bold red]\n")
        
        console.print("[bold red][*][/bold red] [bold white]ALL ACCOUNTS[/bold white] [bold grey74](Run across all loaded credentials)[/bold grey74]")
        if not accounts:
            console.print("    [bold grey74](No saved accounts found. Use Authorizer to add accounts)[/bold grey74]")
        else:
            for idx, acc in enumerate(accounts, 1):
                is_selected = " [bold red]<-- ACTIVE[/bold red]" if current_target == acc['username'] else ""
                console.print(f"[bold red][{idx}][/bold red] [bold white]@{acc['username']}[/bold white] ({acc['status']}){is_selected}")

        console.print("\n[bold red][0][/bold red] [bold grey74]Back to Main Menu[/bold grey74]\n")
        
        choice = Prompt.ask("[bold red]>[/bold red] [bold white]Select Target Account (or '*' for ALL)[/bold white]")
        
        if choice == '0':
            break
        elif choice == '*':
            set_active_target("ALL ACCOUNTS")
            console.print("[bold red]>[/bold red] [bold white]Active target updated to ALL ACCOUNTS[/bold white]")
            time.sleep(1)
            break
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(accounts):
                    selected = accounts[idx]['username']
                    set_active_target(selected)
                    console.print(f"[bold red]>[/bold red] [bold white]Active target updated to @{selected}[/bold white]")
                    time.sleep(1)
                    break
                else:
                    console.print("[bold red]Invalid option.[/bold red]")
                    time.sleep(1)
            except ValueError:
                console.print("[bold red]Please enter a number or '*'[/bold red]")
                time.sleep(1)

def main_menu():
    while True:
        print_banner()
        
        # Load account information and plugins
        accounts = load_accounts()
        active_target = get_active_target()
        plugins = load_plugins()
        plugin_names = list(plugins.keys())
        
        # Clean header status bar (No tables!)
        console.print(f"[bold grey74]ACTIVE TARGET:[/bold grey74] [bold red]{active_target}[/bold red]\n")
        
        console.print("[bold white]--- LOADED PROFILES ---[/bold white]")
        if not accounts:
            console.print(" [bold grey74](No profiles registered)[/bold grey74]")
        else:
            for acc in accounts:
                console.print(f" [bold red]-[/bold red] [bold white]@{acc['username']}[/bold white] [bold grey74]({acc['status']})[/bold grey74]")
        console.print()
        
        console.print("[bold white]--- LOADED PLUGINS ---[/bold white]")
        for idx, p_name in enumerate(plugin_names, 1):
            console.print(f" [bold red][{idx}][/bold red] [bold white]{p_name.capitalize()}[/bold white] [bold grey74](Module Ready)[/bold grey74]")
            
        console.print("\n[bold white]--- CONTROL PANEL ---[/bold white]")
        console.print(" [bold red][A][/bold red] [bold white]Account Manager & Selector[/bold white]")
        console.print(" [bold red][0][/bold red] [bold grey74]Exit Rayzta[/bold grey74]\n")
        
        choice = Prompt.ask("[bold red]>[/bold red] [bold white]Select Option[/bold white]").strip()
        
        if choice == '0':
            console.print("\n[bold grey74]Shutting down Rayzta...[/bold grey74]")
            time.sleep(0.8)
            sys.exit(0)
        elif choice.upper() == 'A':
            account_selector_menu()
        else:
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(plugin_names):
                    selected_plugin_name = plugin_names[choice_idx]
                    plugin_module = plugins[selected_plugin_name]
                    
                    console.print(f"\n[bold grey74]Routing to [/bold grey74][bold white]{selected_plugin_name.capitalize()}[/bold white][bold grey74]...[/bold grey74]")
                    time.sleep(0.6)
                    
                    # Execute the plugin's run method
                    plugin_module.run()
                else:
                    console.print("[bold red]Invalid option. Please try again.[/bold red]")
                    time.sleep(1)
            except ValueError:
                console.print("[bold red]Please enter a valid choice.[/bold red]")
                time.sleep(1)

if __name__ == "__main__":
    try:
        startup_sequence()
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold red]Terminated by user.[/bold red]")
        sys.exit(0)
