import time
from rich.console import Console
from rich.panel import Panel
from core.config_manager import get_favorites, unmark_favorite, mark_favorite
from core.ascii_manager import render_profile_card
import random
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

def execute():
    while True:
        console.clear()
        favorites = get_favorites()
        
        console.print(Panel("[bold white]TARGET MARKER & FAVORITES MANAGER[/bold white]", style="bold red", expand=False))
        console.print(f"[bold grey74]Stored Bookmarked Targets:[/bold grey74] [bold red]{len(favorites)} Favorites[/bold red]\n")
        
        if not favorites:
            console.print("[bold grey74]No bookmarked targets yet. Use 'mark [ID]' in Search or type 'mark <username>' below.[/bold grey74]\n")
        else:
            for idx, fav in enumerate(favorites, 1):
                console.print(f"[bold red]#[ID: {idx}][/bold red]")
                card = render_profile_card(
                    name=fav.get('name', 'Unknown'),
                    username=fav.get('username', 'unknown'),
                    bio=fav.get('bio', 'Favorited Target Profile'),
                    followers=fav.get('followers', 'N/A'),
                    status=fav.get('status', 'Public'),
                    match_score=fav.get('match_score', '100%'),
                    avatar_source=fav.get('image_url')
                )
                console.print(card)
                console.print()

        console.print("[bold grey74]=======================================================[/bold grey74]")
        console.print("[bold red][MARK username][/bold red] Mark target  |  [bold red][UNMARK username/ID][/bold red] Remove target")
        console.print("[bold red][FOLLOW ALL][/bold red] Auto-follow favorites | [bold red][0][/bold red] Main Menu")
        console.print("[bold grey74]=======================================================[/bold grey74]\n")

        cmd = console.input("[bold red]>[/bold red] [bold white]Enter Command:[/bold white] ").strip()
        
        if cmd == '0':
            break
        elif cmd.lower().startswith('unmark'):
            parts = cmd.split(maxsplit=1)
            if len(parts) > 1:
                target_str = parts[1].strip()
                # If number ID passed
                if target_str.isdigit():
                    num = int(target_str) - 1
                    if 0 <= num < len(favorites):
                        u_name = favorites[num]['username']
                        unmark_favorite(u_name)
                        console.print(f"[bold red]>[/bold red] [bold white]Removed @{u_name} from favorites.[/bold white]")
                        time.sleep(1)
                    else:
                        console.print("[bold red]Invalid ID.[/bold red]")
                        time.sleep(1)
                else:
                    if unmark_favorite(target_str):
                        console.print(f"[bold red]>[/bold red] [bold white]Unmarked @{target_str}[/bold white]")
                    else:
                        console.print(f"[bold red]Target @{target_str} was not found in favorites.[/bold red]")
                    time.sleep(1)
            else:
                console.print("[bold red]Usage: unmark <username> or unmark <ID>[/bold red]")
                time.sleep(1)
        elif cmd.lower().startswith('mark'):
            parts = cmd.split(maxsplit=1)
            if len(parts) > 1:
                u_name = parts[1].strip().replace("@", "")
                dummy_profile = {
                    "name": u_name.capitalize(),
                    "username": u_name,
                    "bio": f"Manually bookmarked target @{u_name}",
                    "followers": "Verified",
                    "status": "Public",
                    "match_score": "100%",
                    "image_url": None
                }
                if mark_favorite(dummy_profile):
                    console.print(f"[bold red]>[/bold red] [bold white]Successfully marked @{u_name} as favorite![/bold white]")
                else:
                    console.print(f"[bold grey74]@{u_name} is already in favorites.[/bold grey74]")
                time.sleep(1)
            else:
                console.print("[bold red]Usage: mark <username>[/bold red]")
                time.sleep(1)
        elif cmd.lower() == 'follow all':
            if not favorites:
                console.print("[bold red]No favorites to follow![/bold red]")
                time.sleep(1)
                continue
                
            gap_input = console.input("[bold grey74]Enter gap in seconds (e.g., '10' for fixed, '5-15' for random): [/bold grey74]").strip()
            min_gap, max_gap = 2, 5 # defaults
            
            try:
                if '-' in gap_input:
                    parts = gap_input.split('-')
                    min_gap = int(parts[0].strip())
                    max_gap = int(parts[1].strip())
                elif gap_input.isdigit():
                    min_gap = max_gap = int(gap_input)
            except ValueError:
                console.print("[bold red]Invalid gap format. Using default 2-5 seconds.[/bold red]")
                time.sleep(1)
                
            console.print(f"\n[bold green]Starting Automation: Following {len(favorites)} targets with {min_gap}-{max_gap}s delays...[/bold green]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold white]{task.description}[/bold white]"),
                BarColumn(complete_style="red", finished_style="green"),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console
            ) as progress:
                follow_task = progress.add_task("Following targets...", total=len(favorites))
                
                for fav in favorites:
                    u_name = fav.get("username", "unknown")
                    progress.update(follow_task, description=f"Following @{u_name}...")
                    
                    delay = random.uniform(min_gap, max_gap)
                    time.sleep(delay)
                    
                    progress.advance(follow_task)
                    
            console.print("[bold green]✔ Auto-follow complete![/bold green]")
            console.input("\n[bold grey74]Press Enter to continue...[/bold grey74]")
            
        else:
            console.print("[bold red]Invalid command.[/bold red]")
            time.sleep(0.8)
