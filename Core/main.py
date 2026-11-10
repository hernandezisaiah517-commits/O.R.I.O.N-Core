from commands import COMMANDS, handle_command
from config import load_settings
from local_ai import generate_reply
from logging_setup import setup_logging


MAX_HISTORY_MESSAGES = 12


def main():
    try:
        logger = setup_logging()
    except OSError as error:
        print(f"Could not initialize logging: {error}")
        return

    logger.info("Core starting.")

    try:
        settings = load_settings()
    except (OSError, ValueError) as error:
        logger.exception("Configuration loading failed.")
        print(f"Could not load O.R.I.O.N. settings: {error}")
        return

    assistant_name = settings["assistant_name"]
    user_name = settings["user_name"]
    history = []

    def ask_local(arguments):
        if not arguments.strip():
            return "Usage: ask Your question goes here"

        answer = generate_reply(
            prompt=arguments,
            model=settings["local_model"],
            assistant_name=assistant_name,
            history=history,
        )

        history.append({
            "role": "user",
            "content": arguments,
        })

        history.append({
            "role": "assistant",
            "content": answer,
        })

        del history[:-MAX_HISTORY_MESSAGES]

        return answer

    def reset_conversation(arguments):
        history.clear()
        logger.info("Conversation history cleared.")
        return "Conversation history cleared. Your saved notes are unchanged."

    COMMANDS["ask"] = {
        "handler": ask_local,
        "description": "Ask the local AI: ask Your question",
        "accepts_arguments": True,
    }

    COMMANDS["reset"] = {
        "handler": reset_conversation,
        "description": "Clear the current AI conversation.",
    }

    if settings["show_startup_message"]:
        print(f"{assistant_name} Core")
        print(f"Welcome, {user_name}.")
        print("Type help for commands or exit to stop.")

    logger.info("Command console ready.")

    while True:
        try:
            command = input(f"{user_name}: ").strip()
        except (KeyboardInterrupt, EOFError):
            logger.info("Shutdown requested through console interruption.")
            print(f"\n{assistant_name}: Shutting down.")
            break

        if not command:
            continue

        if command.lower() == "exit":
            logger.info("Shutdown requested through exit command.")
            print(f"{assistant_name}: Shutting down.")
            break

        try:
            response = handle_command(command)
        except KeyboardInterrupt:
            logger.info("Command interrupted.")
            print(f"\n{assistant_name}: Request cancelled.")
            continue
        except (OSError, ValueError) as error:
            logger.exception("Command execution failed.")
            response = f"Could not complete the command: {error}"

        print(f"{assistant_name}: {response}")

    logger.info("Core stopped.")


if __name__ == "__main__":
    main()