from core.discovery import get_available_commands, rank_commands


class CommandRegistry:
    """
    Stores discovered commands in memory so they do not need
    to be rediscovered for every lookup.
    """

    def __init__(self):
        self.commands = []

    def refresh(self):
        """
        Scan the system and reload available commands.
        """

        self.commands = get_available_commands()

    def get_commands(self):
        """
        Return all discovered commands.

        Commands are loaded automatically on the first request.
        """

        if not self.commands:
            self.refresh()

        return self.commands

    def find(self, prefix):
        """
        Find commands matching a prefix.
        """

        commands = self.get_commands()

        prefix = prefix.lower()

        matches = [
            command
            for command in commands
            if command.lower().startswith(prefix)
        ]

        return rank_commands(matches, prefix)