# Contact List - A Database Interface Graphical App
### CS6360 - Database Design Project
#### Rutvij Shah - RDS190000


<br> 

`NOTE: Find detailed docs in ./docs` 

<br>

`NOTE: Change paths in config.py & all .sh files.`

## Technical Requirements

- Language: Python v3.9.5
- Python Packages: `pip install -r requirements.txt`
- Database: SQLite v3.36.0
- GUI Framework: PyQT5
- OS Compatibility: *nix (MacOSX/Linux)
- Miscellaneous: 
  - `pipreqs` to generate requirements file without extraneous specs 
  - `pandoc` for using `document_gen.sh`

## Setup

- Setup a Python 3.9.5+ environment
- Install requirements file
- Create folder `src/generated_views`
- Change the interpreter path in `run.sh` to your local environment.
- Change the database paths in `src/config.py` to your local database location & csv file location.
- Run `build.sh`
  - Builds the python files for UI files in `./ui` and stores them in 
  `src/generated_views`
  - Runs `python3 create_db.py` to create the database
  - Runs `define_text_search.sql` to create a virtual table using FTS5, 
  a module which affords full text-search capabilities in SQLite DBs.
  - Runs `populate_text_search.sql` which populates the text search virtual table with the 
  values already present in the table.
  - Runs `triggers.sql` which adds triggers to all the contact list tables such that
  any CRUD operation on them is replicated & the text search table index is synchronized.

## Application Launch

- Running `main.py` launches the GUI application 
- Find GUI instructions in the `Quickstart Guide`