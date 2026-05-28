import os, hashlib, json
from pathlib import Path

def get_vault_path():
    return Path(__file__).parents[2] / "storage" / "knowledge"

def _hash_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_vault() -> bool:
    manifest_path = get_vault_path() / "manifest.sha256"
    if not manifest_path.exists(): return True
    with manifest_path.open("r") as f:
        stored = json.load(f)
    for rel_path, expected_hash in stored.items():
        full_path = get_vault_path() / rel_path
        if not full_path.is_file() or _hash_file(full_path) != expected_hash:
            return False
    return True

def update_manifest():
    manifest = {}
    vault = get_vault_path()
    for txt in vault.rglob("*.txt"):
        rel = txt.relative_to(vault).as_posix()
        manifest[rel] = _hash_file(txt)
    with (vault / "manifest.sha256").open("w") as f:
        json.dump(manifest, f, indent=2)
