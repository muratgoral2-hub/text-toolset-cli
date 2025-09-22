# 📝 Text Toolset CLI

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20MacOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active-success)

## 📌 Project Purpose
A command-line tool (CLI) for performing batch operations on text files.  
It allows you to quickly read, analyze, edit, and search text files.

---

## 🚀 Features
1. **READ TXT** → Read a file  
2. **WRITE TXT** → Write to a file (overwrite / append)  
3. **ANALYZE TXT** → Count lines, words, and characters  
4. **SHOW WITH LINE NUMBERS** → Display file with line numbers  
5. **SEARCH WORDS IN TXT** → Search for a specific word  
6. **FIND AND REPLACE** → Replace one word with another  
7. **REVERSE TXT** → Reverse the order of lines  
8. **WORD FREQUENCY** → Show the 10 most common words  
9. **ADVANCED SEARCH** → Regex, case, whole word, and context  
10. **HEAD** → Show the first N lines of a file  
11. **TAIL** → Show the last N lines of a file  
12. **UNDO LAST WRITE** → Restore from .bak backup  
13. **EXIT** → Exit the program  

---

## 📂 Installation
```bash
# Clone the repo
git clone https://github.com/yourusername/text-toolset-cli.git
cd text-toolset-cli

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# (Optional) Install extra packages
pip install colorama typer
```

---

## ▶️ How to Run
```bash
# Windows
python main.py

# Mac/Linux
python3 main.py
```

This will launch the interactive menu. Select options by entering the corresponding number (1–13).

---

## ⚡ Usage Examples
```bash
# Read a file
Enter file path : sample.txt

# Write to a file (append)
Enter file path: notes.txt
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
```

---

## 🛠️ Roadmap
- Improve error messages  
- Add colored output (`colorama`)  
- Argument-based usage (`typer` / `argparse`)  
- Logging system (`logging`)  
- Unit tests (`pytest`)  

---

## 👨‍💻 Author
- **Your Name / GitHub link**

---

## 📜 License
This project is distributed under the MIT License.
