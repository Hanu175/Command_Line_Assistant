# Command_Line_Assistant
 
Cross-platform CLI completion and documentation engine — bringing Linux-style command completion and unified documentation support to Windows, macOS, and Linux.

> **Project Name:** CommandPilot
 
---
 
# CommandPilot
 
CommandPilot is a cross-platform command discovery and intelligent CLI completion project.
 
The goal is to build an intelligent layer on top of existing command-line environments that helps users:
 
- Discover installed commands
- Complete partially typed commands
- Understand command-line context
- Discover subcommands and options
- Access documentation through a unified interface
- Reduce repetitive typing
- Work efficiently across Windows, Linux, and macOS
The project does **not** aim to replace existing shells or terminals.
 
Instead, CommandPilot is designed to eventually work alongside environments such as:
 
- Bash
- Zsh
- Fish
- PowerShell
- Windows Command Prompt
---
 
## 🚧 Current Status
 
**Active Development / Early Prototype**
 
CommandPilot currently has a working command discovery and lookup pipeline.
 
The project can:
 
1. Scan the system `PATH`
2. Discover executable commands
3. Filter invalid files
4. Normalize executable names
5. Remove duplicates
6. Match commands using prefixes
7. Rank suggestions
8. Cache discovered commands
9. Refresh the command registry
10. Parse command-line input
11. Identify basic completion context
Current architecture:
 
```text
User Input
    │
    ▼
Command Parser
    │
    ▼
Determine Context
    │
    ├── Command
    ├── Subcommand / Argument
    └── Option
    │
    ▼
Command Registry
    │
    ├── Memory
    ├── Persistent Cache
    └── PATH Discovery
    │
    ▼
Command Suggestions
```
 
---
 
# Features Implemented
 
## 🔍 Command Discovery
 
CommandPilot scans directories available through the system `PATH`.
 
It identifies commands that can be executed from the command line.
 
Example:
 
```bash
python commandpilot.py complete git
```
 
Possible output:
 
```text
git
git-gui
git-lfs
gitk
git-askpass
git-credential-manager
...
```
 
The exact results depend on the software installed on the system.
 
---
 
## ⚡ Prefix-Based Command Matching
 
Users can provide a partial command name.
 
Example:
 
```bash
python commandpilot.py complete dock
```
 
Possible output:
 
```text
docker
docker-compose
docker-credential-desktop
docker-credential-ecr-login
docker-credential-wincred
docker-machine-driver-vmware
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
python3.13
pythonw
pyw
```
 
---
 
## 🪟 Windows Executable Detection
 
On Windows, CommandPilot uses the system `PATHEXT` environment variable to identify executable file types.
 
This prevents non-command files such as:
 
```text
python3.dll
GitHub.dll
DockInterface.ProxyStub.dll
```
 
from appearing as command suggestions.
 
Common executable extensions include:
 
```text
.EXE
.BAT
.CMD
.COM
```
 
The extensions are determined from the system environment rather than being completely hardcoded.
 
---
 
## 🐧 Linux and macOS Compatibility Foundation
 
For Unix-like systems, command discovery is designed around executable permissions rather than Windows executable extensions.
 
This provides the foundation for supporting:
 
* Linux
* macOS
* Other Unix-like environments
Further shell-specific integration will be added in later milestones.
 
---
 
## 🧹 Command Name Normalization
 
Executable extensions are removed from displayed command names.
 
For example:
 
```text
python.exe
```
 
becomes:
 
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
 
This provides cleaner suggestions and helps prevent duplicate command entries.
 
---
 
## 🔁 Duplicate Removal
 
The same command may appear in multiple directories within the system `PATH`.
 
CommandPilot removes duplicate command names so suggestions remain clean.
 
Example:
 
```text
PATH Directory A → python.exe
PATH Directory B → python.exe
```
 
Displayed result:
 
```text
python
```
 
---
 
## 📊 Command Ranking
 
CommandPilot applies a basic rule-based ranking system.
 
The current ranking prioritizes:
 
1. Exact command matches
2. Normal user-facing commands
3. Known helper or internal command patterns
For example:
 
```text
git
```
 
is ranked above helper commands such as:
 
```text
git-askpass
git-credential-manager
git-receive-pack
git-upload-pack
```
 
The current ranking engine is intentionally simple and will later be replaced or extended with more context-aware ranking.
 
---
 
# ⚡ Persistent Command Registry
 
Command discovery can be expensive if the system `PATH` is scanned repeatedly.
 
CommandPilot now includes a `CommandRegistry` that stores discovered commands.
 
The registry uses the following priority:
 
```text
1. Commands already loaded in memory
        ↓
2. Persistent cache
        ↓
3. Fresh PATH scan
```
 
Architecture:
 
```text
CommandPilot
      │
      ▼
Command Registry
      │
      ├── In-Memory Commands
      │
      ├── Persistent Cache
      │
      └── PATH Discovery
```
 
The persistent cache is stored locally:
 
```text
.cache/
└── commands.json
```
 
The cache is machine-specific and is excluded from Git.
 
---
 
## 🔄 Registry Refresh
 
The command registry can be rebuilt manually.
 
```bash
python commandpilot.py refresh
```
 
This forces CommandPilot to:
 
```text
Rescan PATH
    ↓
Rediscover Commands
    ↓
Normalize Commands
    ↓
Remove Duplicates
    ↓
Update commands.json
```
 
Example output:
 
```text
Command registry refreshed. 250 commands discovered.
```
 
The exact number depends on the system.
 
---
 
# 🧠 Command Context Parsing
 
CommandPilot can now begin analyzing a complete command line rather than treating every input as a simple command prefix.
 
For example:
 
```text
git sta
```
 
can be parsed as:
 
```text
Tokens:
["git", "sta"]
 
Command:
git
 
Current Token:
sta
 
Position:
1
 
Context:
subcommand_or_argument
```
 
For:
 
```text
docker --ver
```
 
the parser identifies:
 
```text
Command:
docker
 
Current Token:
--ver
 
Context:
option
```
 
---
 
## ⌨️ Trailing Space Detection
 
A critical requirement for command completion is distinguishing between:
 
```text
git
```
 
and:
 
```text
git␠
```
 
These represent different completion states.
 
### Example 1
 
```text
git
```
 
The user is still typing or completing the command.
 
```text
Context:
command
```
 
### Example 2
 
```text
git 
```
 
The user has completed the command and is requesting the next suggestion.
 
```text
Command:
git
 
Current Token:
""
 
Context:
subcommand_or_option
```
 
This distinction is essential for future `Tab`-based completion.
 
---
 
## 📝 Basic Quote Handling
 
The parser uses Python's `shlex` module to tokenize command-line input.
 
Example:
 
```text
git commit -m "Initial commit"
```
 
Tokens:
 
```text
["git", "commit", "-m", "Initial commit"]
```
 
If incomplete quotes are encountered:
 
```text
git commit -m "Initial
```
 
the parser safely falls back to basic token splitting rather than failing.
 
This is important because command completion often operates while the user is still typing incomplete input.
 
---
 
# How CommandPilot Currently Works
 
The current processing pipeline is:
 
```text
Partial or Complete Command Line
                │
                ▼
          Command Parser
                │
                ▼
      Identify Input Context
                │
        ┌───────┼────────┐
        │       │        │
        ▼       ▼        ▼
     Command  Option  Subcommand /
                        Argument
                │
                ▼
          Command Registry
                │
        ┌───────┼───────────┐
        │       │           │
        ▼       ▼           ▼
      Memory   Cache      PATH Scan
                │
                ▼
          Command List
                │
                ▼
         Prefix Matching
                │
                ▼
        Suggestion Ranking
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
│   ├── discovery.py
│   ├── registry.py
│   └── parser.py
│
├── tests/
│
├── test_parser.py
│
├── .cache/
│   └── commands.json
│
├── README.md
├── requirements.txt
└── .gitignore
```
 
> `.cache/` is generated locally and should not be committed to Git.
 
---
 
# Usage
 
## Complete a Command
 
```bash
python commandpilot.py complete <partial-command>
```
 
Examples:
 
```bash
python commandpilot.py complete git
```
 
```bash
python commandpilot.py complete dock
```
 
```bash
python commandpilot.py complete py
```
 
---
 
## Refresh the Command Registry
 
```bash
python commandpilot.py refresh
```
 
This forces a fresh scan of the system `PATH` and updates the persistent command cache.
 
---
 
# Parser Testing
 
The parser can currently be tested using:
 
```bash
python test_parser.py
```
 
Example test cases include:
 
```text
""
 
"git"
 
"git "
 
"git sta"
 
"git status --short"
 
"git status "
 
"docker"
 
"docker "
 
"docker run"
 
"docker run "
 
"docker --version"
 
"python"
 
"python "
 
"python -m"
 
git commit -m "Initial commit"
 
git commit -m "Initial
```
 
The parser returns information about:
 
* Tokens
* Base command
* Current token
* Token position
* Completion context
---
 
# Development Milestones
 
## ✅ Milestone 0 — Project Foundation
 
Completed.
 
Implemented:
 
* Initial project structure
* Python virtual environment
* CommandPilot entry point
* Core module structure
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
* Executable extension removal
* Duplicate removal
* Basic command ranking
* Lower ranking for helper/internal commands
---
 
## ✅ Milestone 3 — Command Registry
 
Completed.
 
Implemented:
 
* `CommandRegistry` class
* In-memory command storage
* Automatic command loading
* Prefix searching through the registry
* Integration with the existing ranking system
The registry separates command discovery from command lookup.
 
---
 
## ✅ Milestone 4 — Persistent Cache and Registry Refresh
 
Completed.
 
Implemented:
 
* Persistent command cache
* JSON-based storage
* Automatic cache loading
* Automatic fallback to PATH scanning
* Corrupt cache handling
* Manual registry refresh
Command:
 
```bash
python commandpilot.py refresh
```
 
---
 
## 🚧 Milestone 5 — Command Context Parsing
 
**In Progress**
 
Completed so far:
 
* Command-line tokenization
* Command detection
* Current token detection
* Token position detection
* Basic context classification
* Option detection
* Subcommand/argument detection
* Trailing-space detection
* Basic incomplete quote handling
Current context types include:
 
```text
command
option
subcommand_or_argument
subcommand_or_option
argument_or_subcommand
```
 
### Remaining Work
 
The parser will later be improved to support:
 
* Cursor-aware parsing
* Shell-specific quoting rules
* Pipes
* Redirection
* Command chaining
* Environment variables
* Multiple commands on one line
---
 
## ⏭️ Milestone 6 — CLI Capability Discovery
 
**Next Major Phase**
 
This is where CommandPilot begins learning about individual CLI tools.
 
For example:
 
```text
git sta
```
 
The system should determine:
 
```text
Command:
git
 
Current Input:
sta
 
Expected Context:
subcommand
```
 
Then CommandPilot can inspect the CLI and discover possible subcommands.
 
Potential discovery sources:
 
```text
git --help
git -h
git help
```
 
Eventually extracting information such as:
 
```text
add
branch
checkout
clone
commit
log
pull
push
status
stash
```
 
Then:
 
```text
git sta
```
 
could produce:
 
```text
status
stash
```
 
---
 
# Future Goals
 
## ⌨️ Real Shell Integration
 
CommandPilot will eventually integrate with:
 
* Bash
* Zsh
* Fish
* PowerShell
* Windows Command Prompt
The long-term experience could look like:
 
```text
git sta<TAB>
```
 
Suggestions:
 
```text
status
stash
```
 
---
 
## 🌳 CLI Subcommand Completion
 
CommandPilot will learn command structures dynamically.
 
Example:
 
```text
git
├── add
├── branch
├── checkout
├── clone
├── commit
├── log
├── pull
├── push
├── stash
└── status
```
 
---
 
## ⚙️ Option Completion
 
Example:
 
```text
docker --ver
```
 
Potential suggestion:
 
```text
--version
```
 
Another example:
 
```text
git commit --am
```
 
Potential suggestion:
 
```text
--amend
```
 
---
 
## 🔎 Generic CLI Intelligence
 
The goal is to support arbitrary installed CLI tools rather than manually hardcoding every command.
 
Potential information sources include:
 
* Existing shell completion definitions
* CLI-provided completion systems
* `--help`
* `-h`
* `help`
* Native documentation
* Man pages
* PowerShell `Get-Help`
* User-defined metadata
---
 
## 📖 Universal Manual Command
 
A future feature called `manual` will provide a unified documentation interface.
 
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
 
The system will select the most appropriate documentation source.
 
Possible architecture:
 
```text
                manual <command>
                       │
                       ▼
              Documentation Resolver
                       │
         ┌─────────────┼──────────────┐
         │             │              │
         ▼             ▼              ▼
      man pages    Get-Help       CLI --help
       Linux/       PowerShell
       macOS
```
 
The goal is to provide a consistent documentation experience across operating systems.
 
---
 
## 🔍 Fuzzy Matching
 
Future versions should support typo-tolerant completion.
 
Example:
 
```text
doker
```
 
Possible suggestion:
 
```text
docker
```
 
Example:
 
```text
gti
```
 
Possible suggestion:
 
```text
git
```
 
---
 
# Long-Term Architecture
 
```text
                         CommandPilot
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   Completion Engine    Command Discovery      Manual Engine
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                               ▼
                        Command Parser
                               │
                               ▼
                       Command Registry
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
             Memory          Cache         PATH Scan
                               │
                               ▼
                       CLI Intelligence
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
         --help / -h      Completion Files    Native Docs
                               │
                               ▼
                        Command Knowledge
                               │
                               ▼
                         Shell Adapters
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
        Bash              PowerShell              CMD
          │
          ├── Zsh
          │
          └── Fish
```
 
---
 
# Current Limitations
 
CommandPilot is still an early prototype.
 
The current version does **not yet** support:
 
* Real-time `Tab` integration
* Shell adapters
* CLI subcommand discovery
* CLI option discovery
* Argument completion
* `--help` parsing
* Native completion file parsing
* Fuzzy matching
* Cursor-aware completion
* Pipes and redirection parsing
* Command chaining
* The `manual <command>` feature
* Cross-shell installation
* Background registry updates
These capabilities are planned for future milestones.
 
---
 
# Project Goal
 
CommandPilot aims to make command-line environments easier to use without replacing them.
 
The intended workflow is:
 
```text
User Types
    │
    ▼
CommandPilot Understands Context
    │
    ▼
CommandPilot Discovers Available Information
    │
    ├── Commands
    ├── Subcommands
    ├── Options
    ├── Arguments
    └── Documentation
    │
    ▼
Relevant Suggestions
    │
    ▼
Faster and More Discoverable CLI Experience
```
 
The long-term vision is to provide a consistent intelligent completion and documentation layer across:
 
* Windows
* Linux
* macOS
---
 
# Development Status
 
**Current Milestone:** Milestone 5 — Command Context Parsing
 
**Current Progress:** Step 5.3 reached
 
**Next Phase:** Milestone 6 — CLI Capability Discovery
 
**Status:** 🚧 Active Development
