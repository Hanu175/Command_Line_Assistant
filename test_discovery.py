from core.help_discovery import get_command_help


commands = [
    "git",
    "python",
    "docker",
]


for command in commands:
    print("\n" + "=" * 70)
    print(f"COMMAND: {command}")
    print("=" * 70)

    output = get_command_help(command)

    if output:
        print(output[:3000])
    else:
        print("No help output found.")