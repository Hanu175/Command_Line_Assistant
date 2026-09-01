import json
from pathlib import Path

from core.discovery import get_available_commands, rank_commands


class CommandRegistry:
    """
    Stores discovered commands and persists them
    so they can be reused across program executions.
    """

    def __init__(self):
        self.commands = []

        # Project root directory
        project_root = Path(__file__).resolve().parent.parent

        # Cache directory and file
        self.cache_dir = project_root / ".cache"
        self.cache_file = self.cache_dir / "commands.json"

    def refresh(self):
        """
        Scan the system for commands and update the cache.
        """

        self.commands = get_available_commands()

        self.cache_dir.mkdir(exist_ok=True)

        with open(self.cache_file, "w", encoding="utf-8") as file:
            json.dump(
                self.commands,
                file,
                indent=2
            )

        return self.commands

    def load_cache(self):
        """
        Load commands from the persistent cache.
        """

        if not self.cache_file.exists():
            return False

        try:
            with open(self.cache_file, "r", encoding="utf-8") as file:
                self.commands = json.load(file)

            return True

        except (json.JSONDecodeError, OSError):
            return False

    def get_commands(self):
        """
        Return commands.

        Priority:
        1. Commands already in memory
        2. Persistent cache
        3. Fresh system scan
        """

        if self.commands:
            return self.commands

        if self.load_cache():
            return self.commands

        return self.refresh()

    def find(self, prefix):
        """
        Find commands matching a prefix and rank them.
        """

        commands = self.get_commands()

        prefix = prefix.lower()

        matches = [
            command
            for command in commands
            if command.lower().startswith(prefix)
        ]

        return rank_commands(matches, prefix)