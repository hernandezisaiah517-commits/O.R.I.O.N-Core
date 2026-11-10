import json
from pathlib import Path


SETTINGS_FILE = Path(__file__).resolve().parent / "settings.json"

DEFAULT_SETTINGS = {
    "assistant_name": "O.R.I.O.N.",
    "user_name": "Isaiah",
    "show_startup_message": True,
}


def load_settings():
    settings = DEFAULT_SETTINGS.copy()

    if SETTINGS_FILE.exists():
        contents = SETTINGS_FILE.read_text(encoding="utf-8")
        saved_settings = json.loads(contents)

        if not isinstance(saved_settings, dict):
            raise ValueError("Settings must be a JSON object.")

        unknown_keys = saved_settings.keys() - DEFAULT_SETTINGS.keys()

        if unknown_keys:
            names = ", ".join(sorted(unknown_keys))
            raise ValueError(f"Unknown settings: {names}")

        settings.update(saved_settings)

    for key in ("assistant_name", "user_name"):
        value = settings[key]

        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be nonempty text.")

        settings[key] = value.strip()

    if not isinstance(settings["show_startup_message"], bool):
        raise ValueError("show_startup_message must be true or false.")

    return settings