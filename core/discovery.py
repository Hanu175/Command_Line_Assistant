import os


def get_executable_extensions():
    """
    Return executable extensions supported by the current operating system.
    On Windows, these come from the PATHEXT environment variable.
    """

    if os.name == "nt":
        pathext = os.environ.get(
            "PATHEXT",
            ".COM;.EXE;.BAT;.CMD"
        )

        return {
            extension.lower()
            for extension in pathext.split(";")
        }

    # On Linux/macOS, executability is determined by file permissions.
    return set()


def normalize_command_name(filename):
    """
    Remove executable extensions from a command name.
    Example:
        python.exe -> python
        docker.exe -> docker
    """

    executable_extensions = get_executable_extensions()

    name, extension = os.path.splitext(filename)

    if extension.lower() in executable_extensions:
        return name

    return filename


def is_valid_command(full_path, filename):
    """
    Determine whether a file should be treated as a user-runnable command.
    """

    if not os.path.isfile(full_path):
        return False

    # Windows
    if os.name == "nt":
        executable_extensions = get_executable_extensions()

        _, extension = os.path.splitext(filename)

        return extension.lower() in executable_extensions

    # Linux/macOS
    return os.access(full_path, os.X_OK)


def get_available_commands():
    commands = set()

    path_directories = os.environ.get(
        "PATH",
        ""
    ).split(os.pathsep)

    for directory in path_directories:

        if not directory or not os.path.isdir(directory):
            continue

        try:
            for filename in os.listdir(directory):

                full_path = os.path.join(
                    directory,
                    filename
                )

                if is_valid_command(full_path, filename):

                    command_name = normalize_command_name(
                        filename
                    )

                    commands.add(command_name)

        except (PermissionError, OSError):
            continue

    return sorted(commands, key=str.lower)

def rank_commands(commands, prefix):
    """
    Rank commands so that likely primary commands appear first.
    """

    helper_patterns = (
        "-askpass",
        "-credential",
        "-receive-pack",
        "-upload-pack",
        "-helper",
        "-driver",
    )

    def score(command):
        command_lower = command.lower()

        # Exact match is the strongest suggestion.
        if command_lower == prefix.lower():
            return 0

        # Commands containing helper patterns go lower.
        if any(pattern in command_lower for pattern in helper_patterns):
            return 2

        # Normal commands.
        return 1

    return sorted(
        commands,
        key=lambda command: (
            score(command),
            command.lower()
        )
    )

def find_matching_commands(prefix):

    commands = get_available_commands()

    prefix = prefix.lower()

    matches = [
        command
        for command in commands
        if command.lower().startswith(prefix)
    ]

    return rank_commands(matches, prefix)