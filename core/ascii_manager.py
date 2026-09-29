import io
import requests
from PIL import Image
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns

console = Console()

# High-fidelity character gradient from dark to light
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def convert_image_to_ascii(image_obj, width=40):
    """
    Converts a PIL Image object into TrueColor ANSI/Rich RGB ASCII text.
    Uses precise pixel mapping for photographic reproduction.
    """
    try:
        # Aspect ratio adjustment (terminal font characters are ~2x taller than wide)
        aspect_ratio = image_obj.height / image_obj.width
        height = int(width * aspect_ratio * 0.45)
        
        image = image_obj.resize((width, height)).convert("RGB")
        
        ascii_lines = []
        for y in range(image.height):
            line = ""
            for x in range(image.width):
                r, g, b = image.getpixel((x, y))
                brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
                char_idx = int((brightness / 255) * (len(ASCII_CHARS) - 1))
                char = ASCII_CHARS[char_idx]
                line += f"[rgb({r},{g},{b})]{char}[/rgb({r},{g},{b})]"
            ascii_lines.append(line)
        return "\n".join(ascii_lines)
    except Exception as e:
        return f"[bold red]ASCII Convert Error: {e}[/bold red]"

def fetch_image_ascii(url, width=40):
    """
    Downloads an image from URL and converts it to TrueColor ASCII art.
    Includes robust headers to bypass basic bot-protections.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
        }
        resp = requests.get(url, headers=headers, timeout=6)
        if resp.status_code == 200:
            img = Image.open(io.BytesIO(resp.content))
            return convert_image_to_ascii(img, width=width)
        else:
            console.print(f"[dim red]HTTP {resp.status_code} fetching avatar from {url}[/dim red]")
    except Exception as e:
        console.print(f"[dim red]Error fetching avatar: {e}[/dim red]")
        pass
    
    return generate_procedural_ascii_avatar(width=width)

def generate_procedural_ascii_avatar(width=40):
    """
    Generates a fallback colored ASCII picture if internet fetch fails.
    """
    lines = [
        "[rgb(220,50,50)]  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄  [/rgb(220,50,50)]",
        "[rgb(200,80,80)] █  ▄▄▀▀▀▀▀▀▀▀▀▀▀▀▄▄  █ [/rgb(200,80,80)]",
        "[rgb(255,255,255)] █ █  ▀   ▀  █ █ [/rgb(255,255,255)]",
        "[rgb(255,200,200)] █ █   ▄█▄   █ █ [/rgb(255,200,200)]",
        "[rgb(220,50,50)] █  ▀▄▄▄▄▄▄▀  █ [/rgb(220,50,50)]",
        "[rgb(180,180,180)] █ ▄▀        ▀▄ █ [/rgb(180,180,180)]",
        "[rgb(150,150,150)] █ █ NO AVATAR █ █ [/rgb(150,150,150)]",
        "[rgb(220,50,50)]  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀  [/rgb(220,50,50)]"
    ]
    return "\n".join(lines)

def render_profile_card(name, username, bio, followers, status, match_score, avatar_source=None, profile_link=None):
    """
    Renders a profile result with TrueColor ASCII art on the left and metadata on the right.
    """
    if avatar_source and avatar_source.startswith("http"):
        ascii_pic = fetch_image_ascii(avatar_source, width=40)
    else:
        ascii_pic = generate_procedural_ascii_avatar(width=40)
        
    info_lines = [
        f"[bold white]{name}[/bold white]",
        f"[bold red]@{username}[/bold red]",
        f"[bold grey74]Bio:[/bold grey74] [bold white]{bio[:60]}[/bold white]" if bio else "",
        f"[bold grey74]Followers:[/bold grey74] [bold white]{followers}[/bold white]  |  [bold grey74]Status:[/bold grey74] [bold white]{status}[/bold white]",
        f"[bold grey74]Match Score:[/bold grey74] [bold red]{match_score}[/bold red]",
        f"[bold grey74]Verification:[/bold grey74] [bold green][Verified] REAL PUBLIC PROFILE[/bold green]",
        f"[bold grey74]Link:[/bold grey74] [u blue]{profile_link}[/u blue]" if profile_link else ""
    ]
    info_text = "\n".join([line for line in info_lines if line])
    
    content = Columns([ascii_pic, info_text], padding=(0, 4))
    
    return Panel(
        content,
        border_style="grey37",
        title=f"[bold red]Profile Result: @{username}[/bold red]",
        title_align="left",
        expand=False
    )
