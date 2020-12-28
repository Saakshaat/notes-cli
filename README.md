# notes-cli

A Python based CLI for taking notes from your terminal. 

This application was built using [Click](https://click.palletsprojects.com/), which is a wonderful Python package for building interactive CLIs. It uses a SQLite database to save notes in memory and maintains a threshold of (currently) 25 notes. When the total number of notes reaches the threshold, it deletes the oldest note in memory before adding the new note.

# Installation
You must first clone this repository with:
`git clone https://github.com/Saakshaat/notes-cli`

Then, after `cd`ing into its directory, install the executable on your system with:
`pip install --editable .`

If you don't want to have this installed globally, you can run it in a virtual environment. To create a virtual env, go to the repo's directory and on the top-level run
- `virtualenv venv`
- `. venv/bin/activate`
- `pip install --editable .`

# Running

After installing the CLI successfully, you can run it from whichever environment you installed it in with

`notes <command>` 

# Commands
