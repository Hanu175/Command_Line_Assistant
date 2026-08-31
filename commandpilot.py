import sys

from core.discovery import find_matching_commands


def main():
    if len(sys.argv) < 3:
        print("Usage: python commandpilot.py complete <partial-command>")
        return

    action = sys.argv[1]
    partial_command = sys.argv[2]

    if action == "complete":
        matches = find_matching_commands(partial_command)

        for command in matches:
            print(command)

    else:
        print(f"Unknown action: {action}")


if __name__ == "__main__":
    main()