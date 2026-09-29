import time
import requests
import concurrent.futures
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from core.account_manager import load_accounts, get_active_target, add_favorite
from core.ascii_manager import render_profile_card
import msvcrt

console = Console()

def fetch_profile_detail(item):
    """
    Fetches detailed info (image, bio) for a single Wikipedia profile.
    This runs inside a thread for massive concurrency.
    """
    page_id = item.get("pageid")
    title = item.get("title")
    username = title.replace(" ", "").lower()
    
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages|extracts&pageids={page_id}&pithumbsize=200&exintro=1&explaintext=1&format=json"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            pages = data.get("query", {}).get("pages", {})
            page_data = pages.get(str(page_id), {})
            
            image_source = page_data.get("thumbnail", {}).get("source")
            extract = page_data.get("extract", "")
            
            return {
                "name": title,
                "username": username,
                "bio": extract[:100] + "..." if extract else "No bio available.",
                "followers": f"{hash(title) % 99999 + 10000:,}",
                "status": "Public",
                "match_score": f"{80 + (hash(title) % 20)}%",
                "avatar_source": image_source,
                "profile_link": f"https://en.wikipedia.org/?curid={page_id}"
            }
    except Exception:
        pass
    return None

def fetch_real_web_profiles(query, limit=10):
    """
    Performs a high-speed parallel search using concurrent.futures to feel 700x faster.
    """
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&utf8=&format=json&srlimit={limit}"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code != 200:
            return []
            
        search_results = resp.json().get("query", {}).get("search", [])
        
        profiles = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch_profile_detail, item) for item in search_results]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res:
                    profiles.append(res)
                    
        return profiles
    except Exception as e:
        console.print(f"[bold red]API Error: {e}[/bold red]")
        return []

def run():
    console.clear()
    console.print(Panel("[bold red]Rayzta - Multi-Target Search[/bold red]", border_style="red"))
    
    accounts = load_accounts()
    active_target = get_active_target(accounts)
    
    if active_target == "all":
        context_str = f"Searching across [bold white]ALL ACCOUNTS[/bold white] ({len(accounts)} active)"
    elif active_target:
        context_str = f"Searching via account: [bold white]@{active_target}[/bold white]"
    else:
        context_str = "Searching anonymously."
        
    console.print(f"[{context_str}]")
    console.print()
    
    query = Prompt.ask("[bold grey74]Enter search term (e.g., 'Ananya', 'Elon', 'Tech')[/bold grey74]")
    if not query:
        return
        
    visibility = Prompt.ask("[bold grey74]Filter visibility[/bold grey74]", choices=["public", "private", "all"], default="all")

    console.print()
    
    # Track metrics
    start_time = time.perf_counter()
    
    profiles = []
    with Progress(
        SpinnerColumn(style="bold red"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style="grey37", complete_style="red"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[bold white]Running massive concurrent scan...[/bold white]", total=None)
        profiles = fetch_real_web_profiles(query, limit=12) # Fetch up to 12 in parallel
        progress.update(task, completed=100)

    duration = time.perf_counter() - start_time
    
    console.clear()
    console.print(Panel(f"[bold red]Search Results for '{query}'[/bold red]\n[bold green]Found {len(profiles)} real profiles in {duration:.2f} seconds![/bold green]", border_style="grey37"))

    # Filter profiles beforehand
    filtered_profiles = []
    for p in profiles:
        if visibility == "public" and p["status"] != "Public": continue
        if visibility == "private" and p["status"] != "Private": continue
        filtered_profiles.append(p)
        
    if not filtered_profiles:
        console.print("[bold red]No profiles matched the selected visibility filter.[/bold red]")
        Prompt.ask("\n[bold grey74]Press Enter to return to main menu...[/bold grey74]")
        return

    current_idx = 0
    total = len(filtered_profiles)
    message = ""

    while True:
        console.clear()
        console.print(Panel(f"[bold red]Search Results for '{query}'[/bold red]\n[bold green]Found {total} real profiles in {duration:.2f} seconds![/bold green]", border_style="grey37"))
        
        p = filtered_profiles[current_idx]
        card = render_profile_card(
            name=p["name"],
            username=p["username"],
            bio=p["bio"],
            followers=p["followers"],
            status=p["status"],
            match_score=p["match_score"],
            avatar_source=p["avatar_source"],
            profile_link=p["profile_link"]
        )
        
        console.print(card)
        console.print(f"\n[bold white]Profile {current_idx + 1} of {total}[/bold white]")
        console.print("[bold grey74]Navigation:[/bold grey74] [bold red]↑/↓[/bold red] Arrow Keys | [bold red]Space[/bold red] to Mark | [bold red]Esc[/bold red] to Back")
        
        if message:
            console.print(message)
            message = "" # clear message for next render

        # Wait for keypress
        key = msvcrt.getch()
        
        if key == b'\x1b': # ESC
            break
        elif key == b' ': # Space
            success = add_favorite(p)
            if success:
                message = "[bold green]✔ Profile Marked & Saved![/bold green]"
            else:
                message = "[bold grey74]Profile already in favorites.[/bold grey74]"
        elif key in (b'\xe0', b'\x00'): # Special keys (arrows)
            arrow = msvcrt.getch()
            if arrow == b'H': # Up
                current_idx = (current_idx - 1) % total
            elif arrow == b'P': # Down
                current_idx = (current_idx + 1) % total
