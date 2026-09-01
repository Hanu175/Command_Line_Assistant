import sys

from core.registry import CommandRegistry


registry = CommandRegistry()


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python commandpilot.py complete <partial-command>")
        print("  python commandpilot.py refresh")
        return

    action = sys.argv[1]

    if action == "complete":

        if len(sys.argv) < 3:
            print(
                "Usage: "
                "python commandpilot.py complete <partial-command>"
            )
            return

        partial_command = sys.argv[2]

        matches = registry.find(partial_command)

        for command in matches:
            print(command)

    elif action == "refresh":

        commands = registry.refresh()

        print(
            f"Command registry refreshed. "
            f"{len(commands)} commands discovered."
        )

    else:
        print(f"Unknown action: {action}")


if __name__ == "__main__":
    main()