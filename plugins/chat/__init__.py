import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from core.account_manager import get_chatted_users, add_chatted_user
import os

console = Console()

def print_chat_header(target_name="Anonymous"):
    console.clear()
    header = Panel(
        f"[bold red]Rayzta Chat Engine[/bold red] | [bold white]Target:[/bold white] [bold grey74]@{target_name}[/bold grey74]\n"
        "[bold grey74]Status: [bold green]Encrypted Connection Established[/bold green][/bold grey74]",
        border_style="red",
        expand=False
    )
    console.print(header)
    console.print()

def simulate_chat_history(target_name):
    # Fake history for demonstration
    messages = [
        {"sender": "You", "text": f"Hey @{target_name}, I saw your profile.", "color": "red"},
        {"sender": target_name, "text": "Who is this?", "color": "white"},
        {"sender": "You", "text": "Check out this link: https://rayzta-media.com/x49v2", "media": True, "color": "red"},
        {"sender": target_name, "text": "Wait, what is that link?", "color": "white"}
    ]
    
    for msg in messages:
        if msg["sender"] == "You":
            align = "right"
            prefix = "[bold red]You >[/bold red]"
        else:
            align = "left"
            prefix = f"[bold grey74]@{msg['sender']} >[/bold grey74]"
            
        if msg.get("media"):
            text = f"[u blue]{msg['text']}[/u blue]"
        else:
            text = f"[white]{msg['text']}[/white]"
            
        console.print(f"{prefix} {text}")
        time.sleep(0.3)

def run():
    console.clear()
    chatted_users = get_chatted_users()
    
    console.print(Panel("[bold white]CHAT TARGET SELECTOR[/bold white]", style="bold red", expand=False))
    
    if chatted_users:
        console.print("[bold white]--- RECENT CHATS ---[/bold white]")
        for idx, u in enumerate(chatted_users, 1):
            console.print(f"[bold red][{idx}][/bold red] [bold white]@{u}[/bold white]")
        console.print()
    else:
        console.print("[bold grey74]No recent chats found.[/bold grey74]\n")
        
    choice = Prompt.ask("[bold grey74]Enter target username (or select ID from history)[/bold grey74]")
    if not choice:
        return
        
    target_name = choice
    if choice.isdigit() and chatted_users:
        idx = int(choice) - 1
        if 0 <= idx < len(chatted_users):
            target_name = chatted_users[idx]
        else:
            console.print("[bold red]Invalid ID selected.[/bold red]")
            time.sleep(1)
            return
            
    # Add to history
    add_chatted_user(target_name.replace("@", ""))
        
    print_chat_header(target_name)
    
    console.print("[bold grey74]Loading chat history...[/bold grey74]")
    time.sleep(1)
    
    print_chat_header(target_name)
    simulate_chat_history(target_name)
    
    console.print("\n[bold grey74]--- Chat is Live ---[/bold grey74]")
    while True:
        msg = Prompt.ask("[bold red]>[/bold red]")
        if msg.lower() in ['exit', 'quit']:
            break
        
        # Echo the message back locally
        console.print(f"[bold red]You >[/bold red] [white]{msg}[/white]")
        
        # Simulate a typing delay and response from bot
        with console.status("[bold grey74]typing...[/bold grey74]", spinner="dots", spinner_style="red"):
            time.sleep(1.5)
            
        # Fake bot responses based on keywords
        if "hello" in msg.lower():
            reply = "Hi there."
        elif "link" in msg.lower():
            reply = "I'm not clicking any links from strangers."
        else:
            reply = "Interesting. Tell me more."
            
        console.print(f"[bold grey74]@{target_name} >[/bold grey74] [white]{reply}[/white]")
