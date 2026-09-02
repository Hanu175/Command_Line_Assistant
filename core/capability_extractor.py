import re


def extract_options(help_text):
    """
    Extract command-line options from help output.

    Examples:
        --help
        --version
        -h
        -v
    """

    pattern = r"(?<!\w)(--?[a-zA-Z][a-zA-Z0-9_-]*)"

    matches = re.findall(pattern, help_text)

    return sorted(set(matches))


def extract_subcommands(help_text):
    """
    Attempt to extract possible subcommands from
    formatted CLI help output.

    This is an initial generic implementation.
    """

    subcommands = set()

    for line in help_text.splitlines():

        # Match lines that look like:
        #
        #   status     Show repository status
        #   commit     Record changes
        #
        match = re.match(
            r"^\s{2,}([a-zA-Z][a-zA-Z0-9_-]*)\s{2,}",
            line,
        )

        if match:
            candidate = match.group(1)

            # Ignore obvious help headings
            ignored = {
                "usage",
                "options",
                "commands",
                "command",
                "examples",
            }

            if candidate.lower() not in ignored:
                subcommands.add(candidate)

    return sorted(subcommands)


def extract_capabilities(command, help_text):
    """
    Convert raw CLI help output into structured
    capability information.
    """

    return {
        "command": command,
        "subcommands": extract_subcommands(help_text),
        "options": extract_options(help_text),
    }