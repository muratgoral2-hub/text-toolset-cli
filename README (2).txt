TEXT TOOLSET CLI
================

PROJECT PURPOSE
---------------
A command-line tool (CLI) for performing batch operations on text files.
It allows you to quickly read, analyze, edit, and search text files.

FEATURES
--------
1. READ TXT               -> Read a file
2. WRITE TXT              -> Write to a file (overwrite / append)
3. ANALYZE TXT            -> Count lines, words, and characters
4. SHOW WITH LINE NUMBERS -> Display file with line numbers
5. SEARCH WORDS IN TXT    -> Search for a specific word
6. FIND AND REPLACE       -> Replace one word with another
7. REVERSE TXT            -> Reverse the order of lines
8. WORD FREQUENCY         -> Show the 10 most common words
9. ADVANCED SEARCH        -> Regex, case, whole word, and context
10. HEAD                  -> Show the first N lines of a file
11. TAIL                  -> Show the last N lines of a file
12. UNDO LAST WRITE       -> Restore from .bak backup
13. EXIT                  -> Exit the program

INSTALLATION
------------
1. Make sure Python 3.10+ is installed on your system.
2. Navigate to the project folder where main.py is located.

HOW TO RUN
----------
Run the program from the command line:

   python main.py   (Windows)
   python3 main.py  (Mac / Linux)

This will launch the interactive menu. Select options by entering the number (1–13).

USAGE EXAMPLES
--------------
# Read a file
Enter file path : sample.txt

# Write to a file (append mode)
Enter file path : notes.txt
Hello world!
<finish with an empty line>

# Search for a word
Enter file path : sample.txt
Enter the word to search: Python

# Find and replace
word to find: oldword
Replace with: newword

# Reverse file
[OK] reversed file -> sample_reversed.txt

DEVELOPMENT ROADMAP
-------------------
- Improve error messages
- Add colored output (colorama)
- Argument-based usage (typer / argparse)
- Logging system (logging)
- Unit tests (pytest)

LICENSE
-------
This project is distributed under the MIT License.
