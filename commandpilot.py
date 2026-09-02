import sys

from core.registry import CommandRegistry
from core.completion_engine import CompletionEngine


registry = CommandRegistry()
engine = CompletionEngine()


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python commandpilot.py complete <partial-command>")
        print("  python commandpilot.py suggest <command-line>")
        print("  python commandpilot.py refresh")
        return

    action = sys.argv[1]

    # -----------------------------------------
    # Command discovery
    # -----------------------------------------

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

    # -----------------------------------------
    # Context-aware completion
    # -----------------------------------------

    elif action == "suggest":

        if len(sys.argv) < 3:
            print(
                "Usage: "
                'python commandpilot.py suggest "command line"'
            )
            return

        command_line = " ".join(sys.argv[2:])

        suggestions = engine.complete(command_line)

        if suggestions:
            for suggestion in suggestions:
                print(suggestion)
        else:
            print("No suggestions found.")

    # -----------------------------------------
    # Refresh command registry
    # -----------------------------------------

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