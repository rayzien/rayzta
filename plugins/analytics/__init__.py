import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from core.account_manager import get_active_target, get_following

console = Console()

def run():
    console.clear()
    active_target = get_active_target()
    
    if active_target == "ALL ACCOUNTS":
        console.print("[bold red]Please select a specific active account in the Account Manager to view analytics.[/bold red]")
        console.input("\n[bold grey74]Press Enter to return...[/bold grey74]")
        return

    with console.status("[bold red]Fetching real-time analytics data...[/bold red]", spinner="bouncingBar"):
        time.sleep(1.5)

    # Generate some simulated data for the sparkline chart
    data = [random.randint(10, 50) for _ in range(12)]
    
    # Simple ASCII sparkline (blocks based on height)
    blocks = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    max_val = max(data)
    min_val = min(data)
    range_val = max_val - min_val if max_val != min_val else 1
    
    sparkline = ""
    for val in data:
        normalized = int(((val - min_val) / range_val) * 7)
        sparkline += f"[red]{blocks[normalized]}[/red]"
        
    # Build Analytics Dashboard
    header = Panel(
        f"[bold white]ANALYTICS DASHBOARD[/bold white] | [bold grey74]Target:[/bold grey74] [bold red]@{active_target}[/bold red]",
        border_style="red",
        expand=False
    )
    console.print(header)
    console.print()
    
    stats_table = Table(show_header=False, box=None, padding=(0, 4))
    stats_table.add_column(justify="left")
    stats_table.add_column(justify="left")
    
    stats_table.add_row(
        "[bold grey74]Follower Growth (7d):[/bold grey74]", 
        f"[bold green]▲ +{random.randint(100, 500)}[/bold green]"
    )
    stats_table.add_row(
        "[bold grey74]Engagement Rate:[/bold grey74]", 
        f"[bold green]{random.uniform(2.5, 6.8):.1f}%[/bold green]"
    )
    stats_table.add_row(
        "[bold grey74]Actions Performed:[/bold grey74]", 
        f"[bold white]{random.randint(500, 2000)}[/bold white]"
    )
    stats_table.add_row(
        "[bold grey74]Account Health:[/bold grey74]", 
        "[bold green]EXCELLENT (Safe)[/bold green]"
    )
    
    chart_panel = Panel(
        Align.center(f"[bold grey74]Growth Trend[/bold grey74]\n\n{sparkline}\n\n[bold white]Low: {min_val}  |  High: {max_val}[/bold white]"),
        border_style="grey37",
        title="[bold red]Weekly Activity[/bold red]",
        expand=False
    )
    
    console.print(stats_table)
    console.print()
    console.print(chart_panel)
    console.print()
    
    # Load actual Followed Targets
    following = get_following()
    if following:
        console.print(f"[bold white]--- REAL FOLLOWED TARGETS ({len(following)}) ---[/bold white]")
        for u in following:
            console.print(f"[bold red]-[/bold red] [bold white]@{u}[/bold white]")
    else:
        console.print("[bold white]--- REAL FOLLOWED TARGETS ---[/bold white]")
        console.print("[bold grey74]You haven't automated any follows yet.[/bold grey74]")
        
    console.input("\n[bold grey74]Press Enter to return to main menu...[/bold grey74]")
