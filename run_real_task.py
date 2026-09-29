import time
import random
from core.insta_client import get_client
from core.account_manager import add_following, add_chatted_user
from rich.console import Console

console = Console()

def run_automation():
    console.print("[bold green]Starting Real Instagram Automation...[/bold green]")
    cl = get_client()
    if not cl:
        console.print("[bold red]Failed to get client.[/bold red]")
        return
        
    console.print("[bold yellow]--- Task 1: Loading Real Chats ---[/bold yellow]")
    try:
        threads = cl.direct_threads(amount=5)
        for thread in threads:
            users = [u.username for u in thread.users]
            if users:
                target = users[0]
                console.print(f"[bold green]Loaded chat with @{target}[/bold green]")
                add_chatted_user(target)
                
                # Print last message
                if thread.messages:
                    last_msg = thread.messages[0]
                    console.print(f"  [grey74]Last msg:[/grey74] {last_msg.text}")
    except Exception as e:
        console.print(f"[bold red]Failed to load chats: {e}[/bold red]")
        
    console.print("\n[bold yellow]--- Task 2: Following 10 people ---[/bold yellow]")
    keyword = "python"
    try:
        console.print(f"Searching top posts for #{keyword}...")
        medias = cl.hashtag_medias_top(keyword, amount=20)
        
        targets = []
        for m in medias:
            if len(targets) >= 10:
                break
            if m.user.username not in targets:
                targets.append((m.user.username, m.user.pk))
                
        for u_name, u_id in targets:
            console.print(f"Following @{u_name}...")
            try:
                cl.user_follow(u_id)
                add_following(u_name)
                console.print(f"[bold green]✔ Successfully followed @{u_name}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]Failed to follow @{u_name}: {e}[/bold red]")
                
            delay = random.uniform(2, 4)
            time.sleep(delay)
            
    except Exception as e:
        console.print(f"[bold red]Failed during follow campaign: {e}[/bold red]")
        
    console.print("\n[bold green]AUTOMATION COMPLETE[/bold green]")

if __name__ == "__main__":
    run_automation()
