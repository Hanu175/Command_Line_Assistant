# Command_Line_Assistant
Cross-platform CLI completion and documentation engine — brings Linux-style Tab completion and man-style docs to Windows, macOS, and Linux alike.
# CommandPilot

A cross-platform command discovery and intelligent CLI completion project.

CommandPilot aims to improve the command-line experience by helping users discover and complete commands with less typing.

The long-term goal is to create a tool that can integrate with different command-line environments across:

- Windows
- Linux
- macOS

and provide intelligent suggestions based on the commands and CLI tools available on the user's system.

---

## 🚧 Current Status

**Early Development / Proof of Concept**

CommandPilot is currently in its initial development phase.

The first implemented component is the **command discovery engine**, which discovers executable commands available through the system `PATH` and returns relevant suggestions based on partial user input.

```text
User Input
    ↓
git
    ↓
Command Discovery
    ↓
git
git-flow
git-gui
gitk
...
```

---

# Features Implemented

## 🔍 Command Discovery

CommandPilot scans the directories available in the system `PATH`.

It identifies commands that can be executed directly from the command line.

Example:

```bash
python commandpilot.py complete git
```

Possible output:

```text
git
git-flow
git-gui
gitk
```

---

## ⚡ Prefix-Based Command Matching

Users can provide a partial command name.

For example:

```bash
python commandpilot.py complete dock
```

Possible output:

```text
docker
docker-compose
```

Another example:

```bash
python commandpilot.py complete py
```

Possible output:

```text
py
python
python3
pythonw
```

The exact output depends on the commands installed on the user's system.

---

## 🪟 Windows Executable Detection

On Windows, CommandPilot uses the `PATHEXT` environment variable to identify valid executable file types.

This prevents files such as:

```text
python3.dll
GitHub.dll
DockInterface.ProxyStub.dll
```

from appearing as command suggestions.

Executable extensions such as:

```text
.EXE
.BAT
.CMD
.COM
```

are handled dynamically based on the system configuration.

---

## 🧹 Command Name Normalization

Executable extensions are removed from command suggestions.

For example:

```text
python.exe
```

is displayed as:

```text
python
```

Similarly:

```text
docker.exe
```

becomes:

```text
docker
```

This provides cleaner suggestions and prevents duplicate entries.

---

## 📊 Command Ranking

CommandPilot currently applies a basic rule-based ranking system to improve the quality of suggestions.

The ranking prioritizes:

1. Exact command matches
2. Normal user-facing commands
3. Helper or internal commands

For example, when searching for:

```text
git
```

The primary command:

```text
git
```

is ranked above helper executables such as:

```text
git-askpass
git-credential-manager
git-upload-pack
```

The ranking system will be expanded in future milestones.

---

# How It Works

The current command discovery flow is:

```text
Partial User Input
        │
        ▼
Read System PATH
        │
        ▼
Inspect PATH Directories
        │
        ▼
Identify Valid Executables
        │
        ├── Windows
        │     └── Uses PATHEXT
        │
        └── Linux/macOS
              └── Checks executable permissions
        │
        ▼
Normalize Command Names
        │
        ▼
Remove Duplicates
        │
        ▼
Find Prefix Matches
        │
        ▼
Rank Suggestions
        │
        ▼
Return Results
```

---

# Current Project Structure

```text
commandpilot/
│
├── commandpilot.py
│
├── core/
│   ├── __init__.py
│   └── discovery.py
│
├── tests/
│
├── README.md
└── requirements.txt
```

---

# Usage

Run CommandPilot using:

```bash
python commandpilot.py complete <partial-command>
```

Examples:

```bash
python commandpilot.py complete git
```

```bash
python commandpilot.py complete py
```

```bash
python commandpilot.py complete dock
```

---

# Example

### Input

```bash
python commandpilot.py complete dock
```

### Example Output

```text
docker
docker-compose
docker-credential-desktop
docker-credential-ecr-login
docker-credential-wincred
docker-machine-driver-vmware
```

The ranking system prioritizes common user-facing commands while keeping valid helper executables available as lower-priority suggestions.

---

# Development Milestones

## ✅ Milestone 0 — Project Foundation

Completed.

* Created the initial project structure
* Set up a Python virtual environment
* Created the CommandPilot entry point
* Created the core module structure

---

## ✅ Milestone 1 — Command Discovery

Completed.

Implemented:

* System `PATH` scanning
* Executable discovery
* Prefix-based command matching
* Duplicate removal

---

## ✅ Milestone 2 — Clean and Normalize Discovery

Completed.

Implemented:

* Windows executable detection using `PATHEXT`
* Filtering of non-command files such as `.dll`
* Command name normalization
* Removal of executable extensions such as `.exe`
* Duplicate removal
* Basic command ranking
* Lower ranking for helper/internal commands

---

## 🚧 Milestone 3 — Command Registry

**Next milestone.**

The next milestone will introduce a command registry to avoid repeatedly scanning the entire system `PATH`.

Planned functionality:

```python
registry = CommandRegistry()

registry.get_commands()
registry.find("git")
registry.find("dock")
registry.refresh()
```

The registry will provide faster command lookup and create a foundation for future shell completion integration.

---

# Future Goals

## 🔌 Shell Integration

CommandPilot will eventually integrate with existing command-line environments such as:

* Bash
* Zsh
* Fish
* PowerShell
* Windows Command Prompt

The goal is to provide suggestions during normal terminal usage.

Example:

```text
git sta
```

CommandPilot could suggest:

```text
status
stash
```

---

## 🌳 CLI Subcommand Completion

CommandPilot should eventually understand CLI command structures.

Example:

```text
git
 ├── add
 ├── branch
 ├── checkout
 ├── commit
 ├── log
 ├── pull
 ├── push
 └── status
```

The completion engine should then provide context-aware suggestions.

---

## ⚙️ Option Completion

Example:

```text
docker --ver
```

Could suggest:

```text
--version
```

---

## 🔎 Generic CLI Discovery

The project aims to support arbitrary installed CLI tools rather than maintaining a manually hardcoded database for every application.

Potential information sources include:

* Existing shell completion definitions
* CLI-provided completion systems
* `--help`
* `-h`
* `help`
* Native system documentation
* User-defined metadata

---

## 📖 Universal Manual Command

A future feature called `manual` will provide a unified interface for command documentation.

Examples:

```bash
manual git
```

```bash
manual docker
```

```bash
manual ipconfig
```

```powershell
manual Get-Process
```

The tool will attempt to retrieve documentation from the most appropriate source for the current environment.

Possible sources include:

```text
Linux/macOS
    ↓
man pages

PowerShell
    ↓
Get-Help

Generic CLI tools
    ↓
--help
-h
help
```

The goal is to provide a consistent command documentation interface across operating systems.

---

# Long-Term Vision

```text
                     CommandPilot
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        Completion      Command        Manual
          Engine        Discovery       Engine
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                    Command Registry
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          PATH Scan    CLI Help      Completion
                                      Definitions
                           │
                           ▼
                    Command Knowledge
                           │
                           ▼
                     Shell Adapters
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
           Bash           Zsh       PowerShell
```

---

# Current Limitations

CommandPilot is currently a proof of concept.

The current version does **not yet** support:

* Shell `Tab` integration
* CLI subcommand completion
* Command option completion
* Argument/value completion
* `--help` parsing
* The `manual <command>` feature
* Command caching
* Fuzzy matching
* Shell-specific adapters
* Automatic command context detection

These features are planned for future milestones.

---

# Project Goal

CommandPilot does not aim to replace existing shells or terminals.

Instead, it aims to act as an intelligent layer that works alongside existing command-line environments and helps users:

* Discover available commands
* Reduce repetitive typing
* Explore unfamiliar CLI tools
* Complete commands, subcommands, and options
* Access command documentation quickly
* Work more efficiently across different operating systems

---

# Development Status

**Current Milestone:** Milestone 2 Complete

**Next Milestone:** Command Registry and Faster Command Lookup

**Status:** 🚧 Active Development
