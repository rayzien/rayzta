import os
import importlib.util
from rich.console import Console

console = Console()

def load_plugins(plugin_dir="plugins"):
    plugins = {}
    if not os.path.exists(plugin_dir):
        os.makedirs(plugin_dir, exist_ok=True)
        return plugins

    for item in os.listdir(plugin_dir):
        item_path = os.path.join(plugin_dir, item)
        # Check if the item is a folder and contains __init__.py
        if os.path.isdir(item_path):
            init_file = os.path.join(item_path, "__init__.py")
            if os.path.exists(init_file):
                try:
                    # Dynamically load the module
                    spec = importlib.util.spec_from_file_location(f"plugins.{item}", init_file)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # If it has a run() function, it's a valid plugin
                    if hasattr(module, 'run'):
                        plugins[item] = module
                except Exception as e:
                    console.print(f"[bold red]Failed to load plugin '{item}': {e}[/bold red]")
    
    return plugins
