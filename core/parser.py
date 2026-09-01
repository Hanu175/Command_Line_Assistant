import shlex


class CommandContext:
    """
    Represents the parsed state of a command line.
    """

    def __init__(
        self,
        raw_input,
        tokens,
        command,
        current_token,
        position,
        context_type,
    ):
        self.raw_input = raw_input
        self.tokens = tokens
        self.command = command
        self.current_token = current_token
        self.position = position
        self.context_type = context_type

    def __repr__(self):
        return (
            f"CommandContext("
            f"command={self.command!r}, "
            f"current_token={self.current_token!r}, "
            f"position={self.position}, "
            f"context_type={self.context_type!r}"
            f")"
        )

def parse_command_line(command_line):
    """
    Parse a command line and determine what the user
    is currently trying to complete.
    """

    ends_with_space = (
        command_line.endswith(" ")
        or command_line.endswith("\t")
    )

    try:
        tokens = shlex.split(command_line)
    except ValueError:
        # If the command contains incomplete quotes,
        # fall back to basic splitting.
        tokens = command_line.split()

    # Empty command line
    if not tokens:
        return CommandContext(
            raw_input=command_line,
            tokens=[],
            command=None,
            current_token="",
            position=0,
            context_type="command",
        )

    command = tokens[0]

    # Case: user finished the previous token and
    # is starting a new one.
    if ends_with_space:
        current_token = ""
        position = len(tokens)

        if len(tokens) == 1:
            context_type = "subcommand_or_option"
        else:
            context_type = "argument_or_subcommand"

    else:
        current_token = tokens[-1]
        position = len(tokens) - 1

        if len(tokens) == 1:
            context_type = "command"

        elif current_token.startswith("-"):
            context_type = "option"

        else:
            context_type = "subcommand_or_argument"

    return CommandContext(
        raw_input=command_line,
        tokens=tokens,
        command=command,
        current_token=current_token,
        position=position,
        context_type=context_type,
    )