import json
from pathlib import Path


DEFAULT_PET_PATH = Path(__file__).resolve().parents[2] / "pets" / "mochi.json"


def load_pet(path: Path | None = None) -> dict:
    pet_path = path or DEFAULT_PET_PATH
    return json.loads(pet_path.read_text(encoding="utf-8"))
