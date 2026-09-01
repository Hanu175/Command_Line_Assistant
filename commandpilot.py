import sys

from core.registry import CommandRegistry


registry = CommandRegistry()


def main():
    if len(sys.argv) < 3:
        print("Usage: python commandpilot.py complete <partial-command>")
        return

    action = sys.argv[1]
    partial_command = sys.argv[2]

    if action == "complete":
        matches = registry.find(partial_command)

        for command in matches:
            print(command)

    else:
        print(f"Unknown action: {action}")


if __name__ == "__main__":
    main()