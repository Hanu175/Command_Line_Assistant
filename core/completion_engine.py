from core.parser import parse_command_line
from core.registry import CommandRegistry
from core.help_discovery import get_command_help
from core.capability_extractor import extract_capabilities


class CompletionEngine:
    """
    Coordinates command discovery, parsing, capability
    discovery, and suggestion generation.
    """

    def __init__(self):
        self.registry = CommandRegistry()

    def complete(self, command_line):
        """
        Return completion suggestions based on the
        current command-line context.
        """

        context = parse_command_line(command_line)

        # Empty input
        if not context.command:
            return []

        # -------------------------------------------------
        # CASE 1: Completing the executable command itself
        # -------------------------------------------------

        if context.context_type == "command":

            return self.registry.find(
                context.current_token
            )

        # -------------------------------------------------
        # CASE 2: Completing something inside a command
        # -------------------------------------------------

        capabilities = self._get_capabilities(
            context.command
        )

        if not capabilities:
            return []

        current_token = context.current_token.lower()

        suggestions = []

        # If the user is typing an option
        if context.context_type == "option":

            suggestions = [
                option
                for option in capabilities["options"]
                if option.lower().startswith(current_token)
            ]

        # If the user is typing a possible subcommand
        elif context.context_type in {
            "subcommand_or_argument",
            "subcommand_or_option",
            "argument_or_subcommand",
        }:

            suggestions = [
                subcommand
                for subcommand in capabilities["subcommands"]
                if subcommand.lower().startswith(current_token)
            ]

            # If no subcommand matches, also check options.
            if not suggestions:

                suggestions = [
                    option
                    for option in capabilities["options"]
                    if option.lower().startswith(current_token)
                ]

        return sorted(suggestions)

    def _get_capabilities(self, command):
        """
        Retrieve and extract capabilities for a command.
        """

        help_text = get_command_help(command)

        if not help_text:
            return None

        return extract_capabilities(
            command,
            help_text,
        )