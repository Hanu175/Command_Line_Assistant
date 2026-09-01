from core.parser import parse_command_line


examples = [
    "",
    "git",
    "git sta",
    "git status --short",
    "docker",
    "docker run",
    "docker --version",
    "python -m",
    'git commit -m "Initial commit"',
    'git commit -m "Initial',
]


for example in examples:
    context = parse_command_line(example)

    print("=" * 50)
    print("Input:        ", repr(example))
    print("Tokens:       ", context.tokens)
    print("Command:      ", context.command)
    print("Current token:", context.current_token)
    print("Position:     ", context.position)
    print("Context type: ", context.context_type)