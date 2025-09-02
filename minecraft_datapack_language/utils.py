
import os, json
from pathlib import Path

def ensure_dir(p: str):
    Path(p).mkdir(parents=True, exist_ok=True)

def write_json(path: str, data: dict):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def write_text(path: str, text: str):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.rstrip() + "\n")

def ns_path(namespace: str, path: str) -> str:
    if ":" in path:
        raise ValueError("Path should be relative (no namespace).")
    if path.startswith("/"):
        path = path[1:]
    return f"{namespace}/{path}"

def find_mdl_files(directory: Path) -> list[Path]:
    """Find all .mdl files in a directory recursively.
    
    Args:
        directory: Directory to search in
        
    Returns:
        List of Path objects for .mdl files
    """
    mdl_files = []
    for item in directory.rglob("*.mdl"):
        if item.is_file():
            mdl_files.append(item)
    return sorted(mdl_files)
