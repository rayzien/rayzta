import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from core.account_manager import add_following
from core.insta_client import get_client

console = Console()

def run():
    console.clear()
    
    header = Panel(
        "[bold white]FOLLOW MANAGER MODULE[/bold white]\n"
        "[bold grey74]Automate your growth by following active users based on Hashtags or Topics.[/bold grey74]",
        border_style="red",
        expand=False
    )
    console.print(header)
    console.print()
    
    keyword = Prompt.ask("[bold red]>[/bold red] [bold white]Enter Topic or Hashtag (e.g., #tech, marketing)[/bold white]")
    if not keyword:
        return
        
    count_str = Prompt.ask("[bold red]>[/bold red] [bold white]How many users to follow?[/bold white]", default="10")
    try:
        count = int(count_str)
    except ValueError:
        console.print("[bold red]Invalid number. Defaulting to 10.[/bold red]")
        count = 10
        
    gap_input = Prompt.ask("[bold red]>[/bold red] [bold white]Enter gap in seconds (e.g., '10' for fixed, '5-15' for random)[/bold white]", default="5-15")
    min_gap, max_gap = 5, 15
    try:
        if '-' in gap_input:
            parts = gap_input.split('-')
            min_gap = int(parts[0].strip())
            max_gap = int(parts[1].strip())
        elif gap_input.isdigit():
            min_gap = max_gap = int(gap_input)
    except Exception:
        console.print("[bold red]Invalid gap format. Using default 5-15 seconds.[/bold red]")
        min_gap, max_gap = 5, 15
        
    console.print(f"\n[bold grey74]Searching Instagram for hashtag '{keyword.replace('#', '')}'...[/bold grey74]")
    
    cl = get_client()
    if not cl:
        return
        
    real_profiles = []
    with console.status("[bold red]Scraping medias from hashtag...[/bold red]", spinner="bouncingBar"):
        try:
            # Get top medias for hashtag
            medias = cl.hashtag_medias_top(keyword.replace('#', ''), amount=count * 2)
            for m in medias:
                if len(real_profiles) >= count:
                    break
                if m.user.username not in real_profiles:
                    real_profiles.append(m.user)
        except Exception as e:
            console.print(f"[bold red]API Error: {e}[/bold red]")
            return
            
    if not real_profiles:
        console.print("[bold red]No targets found for that keyword![/bold red]")
        console.input("\n[bold grey74]Press Enter to return...[/bold grey74]")
        return
        
    console.print(f"[bold green]✔ Found {len(real_profiles)} highly-engaged REAL Instagram targets![/bold green]\n")
    console.print(f"[bold red]Starting Automation:[/bold red] [bold white]Following {len(real_profiles)} targets with {min_gap}-{max_gap}s delays...[/bold white]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold white]{task.description}[/bold white]"),
        BarColumn(complete_style="red", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        follow_task = progress.add_task("Following targets...", total=len(real_profiles))
        
        for user_obj in real_profiles:
            u_name = user_obj.username
            u_id = user_obj.pk
            progress.update(follow_task, description=f"Following @{u_name}...")
            
            try:
                # REAL INSTAGRAM FOLLOW
                cl.user_follow(u_id)
            except Exception as e:
                console.print(f"\n[bold red]Failed to follow @{u_name}: {e}[/bold red]")
                
            delay = random.uniform(min_gap, max_gap)
            time.sleep(delay)
            
            # Save it to the database!
            add_following(u_name)
            
            progress.advance(follow_task)
            
    console.print("\n[bold green]✔ Automated Follow Campaign Complete![/bold green]")
    console.input("\n[bold grey74]Press Enter to return to main menu...[/bold grey74]")
