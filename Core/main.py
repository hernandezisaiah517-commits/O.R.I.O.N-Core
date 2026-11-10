from commands import handle_command


def main():
    print("O.R.I.O.N. Core")
    print("Type help for commands or exit to stop.")

    while True:
        try:
            command = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nO.R.I.O.N.: Shutting down.")
            break

        if not command:
            continue

        if command.lower() == "exit":
            print("O.R.I.O.N.: Shutting down.")
            break

        try:
            response = handle_command(command)
        except (OSError, ValueError) as error:
            response = f"Could not complete the command: {error}"

        print(f"O.R.I.O.N.: {response}")


if __name__ == "__main__":
    main()