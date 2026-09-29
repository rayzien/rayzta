import os
import json
import time
from plugins.search import fetch_real_web_profiles
from core.ascii_manager import render_profile_card
from rich.console import Console

console = Console()

def test():
    start_time = time.perf_counter()
    profiles = fetch_real_web_profiles("Elon Musk", limit=3)
    duration = time.perf_counter() - start_time
    
    print(f"Found {len(profiles)} profiles in {duration:.2f} seconds.")
    for p in profiles:
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

if __name__ == "__main__":
    test()
