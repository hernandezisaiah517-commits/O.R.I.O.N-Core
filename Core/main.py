from commands import handle_command
from config import load_settings


def main():
    try:
        settings = load_settings()
    except (OSError, ValueError) as error:
        print(f"Could not load O.R.I.O.N. settings: {error}")
        return

    assistant_name = settings["assistant_name"]
    user_name = settings["user_name"]

    if settings["show_startup_message"]:
        print(f"{assistant_name} Core")
        print(f"Welcome, {user_name}.")
        print("Type help for commands or exit to stop.")

    while True:
        try:
            command = input(f"{user_name}: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{assistant_name}: Shutting down.")
            break

        if not command:
            continue

        if command.lower() == "exit":
            print(f"{assistant_name}: Shutting down.")
            break

        try:
            response = handle_command(command)
        except (OSError, ValueError) as error:
            response = f"Could not complete the command: {error}"

        print(f"{assistant_name}: {response}")


if __name__ == "__main__":
    main()