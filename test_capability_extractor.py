from core.help_discovery import get_command_help
from core.capability_extractor import extract_capabilities


commands = [
    "git",
    "docker",
    "python",
]


for command in commands:

    print("\n" + "=" * 70)
    print(f"COMMAND: {command}")
    print("=" * 70)

    help_text = get_command_help(command)

    if not help_text:
        print("No help output found.")
        continue

    capabilities = extract_capabilities(
        command,
        help_text,
    )

    print("\nSUBCOMMANDS:")

    for subcommand in capabilities["subcommands"]:
        print(f"  {subcommand}")

    print("\nOPTIONS:")

    for option in capabilities["options"]:
        print(f"  {option}")