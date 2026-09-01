# from core.discovery import (
#     get_available_commands,
#     find_matching_commands,
# )


# class CommandRegistry:
#     """
#     Stores discovered commands in memory so they do not need
#     to be rediscovered for every lookup.
#     """

#     def __init__(self):
#         self.commands = []

#     def refresh(self):
#         """
#         Scan the system and reload available commands.
#         """

#         self.commands = get_available_commands()

#     def get_commands(self):
#         """
#         Return all commands.

#         If commands have not been loaded yet,
#         load them first.
#         """

#         if not self.commands:
#             self.refresh()

#         return self.commands

#     def find(self, prefix):
#         """
#         Find commands matching a prefix using the registry.
#         """

#         commands = self.get_commands()

#         prefix = prefix.lower()

#         matches = [
#             command
#             for command in commands
#             if command.lower().startswith(prefix)
#         ]

#         return matches

from core.discovery import get_available_commands


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
        Return all commands.

        If commands have not been loaded yet,
        load them first.
        """

        if not self.commands:
            self.refresh()

        return self.commands

    def find(self, prefix):
        """
        Find commands matching a prefix using the registry.
        """

        commands = self.get_commands()

        prefix = prefix.lower()

        return [
            command
            for command in commands
            if command.lower().startswith(prefix)
        ]