import json
from pathlib import Path
import hashlib
from typing import List, Dict, Optional

from config import DOCS_PATH, MANIFEST_PATH, ALLOWED_EXTS


def _load_manifest(manifest_path: Path) -> Dict:
    if not manifest_path.exists():
        return {"files": {}}
    return json.loads(manifest_path.read_text(encoding="utf-8"))

def _save_manifest(manifest_path: Path, manifest: Dict):
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def _compute_file_hash(path: Path) -> str:
    """SHA256 of file contents for change detection."""

    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            h.update(block)
    return h.hexdigest()


def changed_files(docs_path: Path, manifest_path: Path) -> List[Path]:
    files = [
        p for p in docs_path.rglob("*")
        if p.is_file()
        and p.suffix.lower() in ALLOWED_EXTS
        and not any(i.startswith('.') for i in p.parts)
    ]

    old_manifest = _load_manifest(manifest_path)
    old_files = old_manifest.get("files", {})

    current_files = {}
    changed_files = []

    for path in files:
        fhash = _compute_file_hash(path)
        current_files[str(path)] = fhash
        if old_files.get(str(path)) != fhash:
            changed_files.append(path)

    if not changed_files:
        print("No changed files since last run. Nothing to index.")
        # Still update manifest config if needed
        new_manifest = {
            "files": current_files,
        }
        _save_manifest(manifest_path, new_manifest)

    new_manifest = {
        "files": current_files,
    }
    _save_manifest(manifest_path, new_manifest)

    return changed_files

    # new_manifest["files"] = file_paths
    # _save_manifest(manifest_path, new_manifest)

if __name__ == "__main__":
    pass