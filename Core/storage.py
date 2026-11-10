import json
from pathlib import Path


DATA_DIRECTORY = Path(__file__).resolve().parent / "data"
NOTES_FILE = DATA_DIRECTORY / "notes.json"


def load_notes():
    if not NOTES_FILE.exists():
        return []

    contents = NOTES_FILE.read_text(encoding="utf-8")
    notes = json.loads(contents)

    if not isinstance(notes, list):
        raise ValueError("The notes file must contain a list.")

    if not all(isinstance(note, str) for note in notes):
        raise ValueError("Every saved note must be text.")

    return notes


def save_note(text):
    notes = load_notes()
    notes.append(text)

    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    contents = json.dumps(notes, indent=2)
    NOTES_FILE.write_text(contents, encoding="utf-8")

    return len(notes)