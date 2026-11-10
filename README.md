# O.R.I.O.N.

A personal assistant project with a shared software core and
planned home control, helmet, and glasses interfaces.

## Current functionality

The core currently provides a local text console with:

- Command help
- Console status
- Local time and date
- Persistent notes
- Basic input and storage error handling

## Project areas

- Core: shared assistant software
- Home Control: planned home integrations
- Helmet: planned helmet interface
- Glasses: planned glasses interface

## Development environment

- Python 3
- Visual Studio Code
- Git

The current core uses only Python's standard library.
No third-party Python packages are required yet.

Create a virtual environment inside Core:

    py -m venv .venv

Select that environment as the Python interpreter in VS Code.

## Running the core

From Core, with the virtual environment activated:

    python main.py

## Commands

| Command | Purpose |
|---|---|
| help | List available commands |
| status | Show console status |
| time | Show local time |
| date | Show local date |
| note Your text | Save a note |
| notes | Display saved notes |
| exit | Stop the console |

## Local data

Notes are saved automatically in Core's data folder.

The virtual environment, saved notes, Python cache files,
and local environment configuration are excluded through
Core's .gitignore.

## Development approach

Build and verify the core first, then connect the other interfaces.