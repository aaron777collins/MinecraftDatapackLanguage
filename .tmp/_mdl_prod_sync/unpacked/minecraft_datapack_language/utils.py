
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
