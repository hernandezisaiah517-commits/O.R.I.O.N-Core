from datetime import datetime

from storage import load_notes, save_note


def show_help(arguments):
    lines = ["Available commands:"]

    for name, details in COMMANDS.items():
        lines.append(f"  {name}: {details['description']}")

    lines.append("  exit: Stop O.R.I.O.N.")
    return "\n".join(lines)


def show_status(arguments):
    return "The command console is running. Local note storage is enabled."


def show_time(arguments):
    return datetime.now().strftime("The time is %I:%M %p.")


def show_date(arguments):
    return datetime.now().strftime("Today is %A, %B %d, %Y.")


def create_note(arguments):
    if not arguments:
        return "Usage: note Your note goes here"

    count = save_note(arguments)
    return f"Note saved. Total notes: {count}."


def show_notes(arguments):
    notes = load_notes()

    if not notes:
        return "You have no saved notes yet."

    lines = ["Your notes:"]

    for number, text in enumerate(notes, start=1):
        lines.append(f"{number}. {text}")

    return "\n".join(lines)


COMMANDS = {
    "help": {
        "handler": show_help,
        "description": "List available commands.",
    },
    "status": {
        "handler": show_status,
        "description": "Check the console.",
    },
    "time": {
        "handler": show_time,
        "description": "Show the local time.",
    },
    "date": {
        "handler": show_date,
        "description": "Show the local date.",
    },
    "note": {
        "handler": create_note,
        "description": "Save a note: note Your text",
        "accepts_arguments": True,
    },
    "notes": {
        "handler": show_notes,
        "description": "Show saved notes.",
    },
}


def handle_command(command):
    name, separator, arguments = command.partition(" ")
    name = name.lower()
    arguments = arguments.strip()

    details = COMMANDS.get(name)

    if details is None:
        return "Unknown command. Type help to see available commands."

    if arguments and not details.get("accepts_arguments", False):
        return f"The {name} command does not take additional text."

    handler = details["handler"]
    return handler(arguments)