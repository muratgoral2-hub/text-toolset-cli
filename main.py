# ==============================
# Komut Satırı Araç Seti (CLI)
# Amaç: Metin dosyaları üzerinde toplu işlemler yapmak
# Özellikler:
# 1. Dosya okuma
# 2. Dosya yazma
# 3. Dosya analizi (satır, kelime, karakter sayısı)
# 4. Satır numaralarıyla gösterme
# 5. Dosyada kelime arama
# 6. Bul-Değiştir
# 7. Dosyayı ters çevirme
# 8. Kelime sıklığı analizi
# ==============================
# Kullanıcıdan isim alıp karşılama yapan fonksiyon

import re
import os
import tempfile
from pathlib import Path
from collections import Counter

# ===========================================
# EKLENDİ: Akıllı okuma ve güvenli yazma yardımcıları
# - Notepad (UTF-16/ANSI) / UTF-8 BOM / UTF-8 dosyaları doğru okur
# - Satır sonlarını normalize eder (CRLF/CR -> LF)
# - Yazarken .bak yedeği ve atomik replace yapar
# ===========================================

def _detect_encoding(path: str) -> str:

    p= Path(path)
    raw=p.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    if raw.startswith((b"\xff\xfe",b"\xfe\xff")):
        return "utf-16"
    try:
        raw.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "cp1254"
def _read_text_smart(path:str) -> tuple[str, str]:
    enc=_detect_encoding(path)
    text= Path(path).read_bytes().decode(enc, errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text, enc

def _safe_write(path: str, data: str, backup: bool = True):
        p = Path(path)
        if backup and p.exists():
            p.with_suffix(p.suffix + ".bak").write_bytes(p.read_bytes())
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", errors="replace", newline="") as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        os.replace(tmp_path, p)

def _collect_lines(promt: str) -> tuple[str, int]:
    print(promt)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line =="" :
            break
        lines.append(line)
    data = "\n".join(lines) + ("\n" if lines else "")
    return data, len(lines)
def _append_text(p: Path, data: str):
    if p.exists():
        old, _ = _read_text_smart(p)
        joiner= "" if (not old or old.endswith("\n")) else "\n"
        new_content = old + joiner + data
        _safe_write(p, new_content, backup=True)
    else:
        _safe_write(p, data, backup=True)
#Gelişmiş arama regex, case, whole word, context
def search_advanced(path,query,*,regex=False, ignore_case=True, whole_word=False, context=0):
    try:
        content, _ = _read_text_smart(path)
    except FileNotFoundError:
        print("File not found")
        return
    except (PermissionError, UnicodeDecodeError):
        print("File cant read")
        return
    flags = re.IGNORECASE if ignore_case else 0
    if regex:
        try:
            pattern = re.compile(query, flags)
        except re.error as e:
            print(f"Invalid regex: {e}")
            return
    else:
        pattern = re.compile(term, flags)
    lines = content.split("\n")
    width =len(str(len(lines))) or 1
    found= False
    for i,line in enumerate(lines, start=1):
        if pattern.search(line):
            found=True
            start = max(1, i - context)
            end = min(len(lines), i + context)
            for j in range(start, end + 1):
                prefix = ">" if j == i else ""
                print(f"{prefix}{j:{width}}: {lines[j-1]}")
            if context and end < len(lines):
                print("--")
    if not found:
        print("--")
# Head N ilk satır

def head(path, n = 10):
    try:
        content, _ = _read_text_smart(path)
        for line in content.split("\n")[:n]:
            print(line)
    except FileNotFoundError:
        print("File not found")
# Tail N son satır

def tail(path, n = 10):
    try:
        content, _ = _read_text_smart(path)
        lines = content.split("\n")
        for line in lines[-n]:
            print(line)
    except FileNotFoundError:
        print("File not found")
#Undo .baktan geri al

def undo_last_write(path):
    p = Path(path)
    bak = p.with_suffix(p.suffix + ".bak")
    if not bak.exists():
        print("No backup (.bak) found")
        return
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
        tmp.write(bak.read_bytes())
        tmp_path = tmp.name
    os.replace(tmp_path, p)
    print("Restored from {bak.resolve()} -> {p.resolve()}")


def welcome():
    name = input("What is your name:")
    print(f"Hello {name}, Welcome to Mini Command Prompt\n")

# Bir dosyayı ekrana yazdırma

def txt_read(text):
    try:
        content, enc=_read_text_smart(text)
        print(f"\n---inside of txt--- ({Path(text).resolve()}) [encoding={enc}]")
        print(content, end="")
    except FileNotFoundError:
        print("\nFile not found")

# Bir dosyaya yazı ekleme
def txt_write(text):
    data, nlines = _collect_lines("Type content (Finish with empty line).")
    p = Path(text)
    if p.exists():
        ans = input(f"'{p.resolve()}' exists. Choose: [0]verwrite / [A]ppend / [C]ancel: ").strip().lower()
        if ans.startswith("c"):
            print("Option cancelled")
            return
        elif ans.startswith("a"):
            _append_text(p, data)
            print(f"\nAppended {nlines} line(s) to '{p.resolve()}'")
            return
        elif not ans.startswith("0"):
            print("Option error")
            return
    _safe_write(p, data, backup=True)
    print(f"\nText written successfully -> {p.resolve()} (lines:{nlines})")

    print("Type content (Finish with empty line):")
    lines = []
    while True:
        try:
            line=input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)
    data="\n".join(lines) + ("\n" if lines else "")
    p = Path(text)
    if p.exists():
        ans =input(f"'{p.resolve()}' already exists. Would you like to overwrite it? (y/n): ").strip().lower()

        _safe_write(p, data, backup=True)
        print(f"\nText written successfully {p.resolve()}")

        return
    _safe_write(p, data, backup=True)
    print(f"\nText written successfully {p.resolve()}")

# Dosyanın satır, kelime ve karakter sayısını hesaplama



def text_analysis(text):
    try:
        content, _ = _read_text_smart(text)
        lines=len(content.split("\n"))
        words=len(re.findall(r"\b[\w+']+\b", content))
        chars=len(content)
        print(f"{text}\nLines: {lines}, Words: {words}, Characters: {chars}")
    except (FileNotFoundError, PermissionError,UnicodeDecodeError) as e:
        print("\nFile cant analysis")


# Dosyada belirli bir kelimeyi arama

def word_search(text , word):
    try:
        content, _ = _read_text_smart(text)
    except (FileNotFoundError):
        print("\nFile not found")
        return
    except (PermissionError, UnicodeDecodeError):
        print("\nFile cant read")
        return
    pattern = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
    found = False
    for i, line in enumerate(content.split("\n"),start=1):
        if pattern.search(line):
            print(f"{i}:{line.strip()}")
            found = True
    if not found:
        print("\nNo such word")
#Satırları numaralı göster

def show_with_line_numbers(text):
    try:
        content, _ = _read_text_smart(text)
        lines=content.split("\n")
        if lines and lines[-1]=="":
            lines=lines[:-1]
        width = len(str(len(lines))) or 1
        for i,line in enumerate(lines, start=1):
            print(f"{i:> {width}}: {line.rstrip()}")
    except FileNotFoundError:
        print("\nFile not found")

#Atladığım özellik

def findandreplace(text, old, new):
    try:
        content, _ = _read_text_smart(text)
        pattern = re.compile(rf"\b{re.escape(old)}\b", re.IGNORECASE)
        matches = list(pattern.finditer(content))
        if matches:
            replaced = pattern.sub(new, content)
            _safe_write(text, replaced, backup=True)
            print(f"{len(matches)}  occurence(s) of '{old}' replaced with '{new}'")
        else:
            print("Word not found in text")
    except FileNotFoundError:
        print("File cannot be found")
# Dosyada kelimeyi bulup başka kelimeyle değiştirme




# Dosyadaki satırları sondan başa çevirme

def opposite(text, output=None, enc=None):
    try:
        content, enc = _read_text_smart(text)
        lines = content.split("\n")
        if lines and lines [-1] == "" :
            lines = lines[:-1]
        reversed_text = "\n".join(reversed(lines)) + "\n"
        if output is None:

            p=Path(text)
            output= p.with_name(p.stem + "_reversed" + p.suffix)
        else:
            output= Path(output)
        _safe_write(output, reversed_text, backup=False)

        print(f"[OK] reversed file (encoding={enc}) -> {output.resolve()} ")
    except FileNotFoundError:
        print(f"[ERROR] file not found: {Path(text).resolve()}")
    except Exception as e:
        print(f"[ERROR] reverse failed: {e}")

# Dosyada geçen kelimelerin sayısını bulma

def word_frequency(text):
    try:
        content, _ = _read_text_smart(text)
        tokens=re.findall(r"\b[\w']+\b", content.lower())
        freqs = Counter(tokens)
        print("Most Common Words: ")
        for word, quantitiy in freqs.most_common(10):
            print(f"{word}: {quantitiy}")
    except FileNotFoundError:
        print("File cannot be found")


# En çok geçen 10 kelimeyi sıralar



# Programın menüsü

def menu():
    welcome()
    while True:
        print("""
        ===TEXT TOOLSET===
        1. READ TXT
        2. WRITE TXT (OVERWRITE AND APPEND)
        3. ANALYZE TXT
        4. SHOW TEXT WITH LINES NUMBERS
        5. SEARCH WORDS IN TXT
        6. FIND AND REPLACE
        7. REVERSE TXT
        8. WORD FREQUENCY ANALYSIS
        9. ADVANCED SEARCH (regex, case, context)
        10. SHOW HEAD (First n lines)
        11. SHOW TAİL (Last n lines)
        12. UNDO LAST WRITE (Restore from .bak)
        13. EXIT
        """)
        try:

            selection = input("Enter your selection (1-9): "). strip()
        except(KeyboardInterrupt, EOFError):
            print("\nExiting")
            break

        # Menü seçimlerine göre fonksiyon çağrısı

        if selection == "1":
            text = input("Enter file path : ")
            txt_read(text)
        elif selection == "2":
            text = input("Enter file path: ")
            txt_write(text)
        elif selection == "3":
            text = input("Enter file path: ")
            text_analysis(text)
        elif selection == "4":
            text = input("Enter file path: ")
            show_with_line_numbers(text)
        elif selection == "5":
            text = input("Enter file path: ")
            word = input("Enter the word to search: ")
            word_search(text, word)
        elif selection == "6":
            text = input("Enter file path: ")
            old = input("word to find: ")
            new = input("Replace with: ")
            findandreplace(text, old, new)
        elif selection == "7":
            text = input("Enter file path: ")
            opposite(text)
        elif selection == "8":
            text = input("Enter file path: ")
            word_frequency(text)
        elif selection == "9":
            text = input("Enter file path: ").strip()
            q=input("Enter file path: ").strip()
            regex = input("Regex? (y/n):").strip().lower().startswith("y")
            case_sens = input("Case sensitive? (y/n):").strip().lower().startswith("y")
            whole = input("whole word? (y/n): ").strip().lower().startswith("y")
            try:
                ctx = int((input("Context lines (0..10):").strip() or "0"))
            except :
                ctx = 0
            search_advanced(text, q, regex=regex, ignore_case=not case_sens, whole_word=whole, context=ctx )
        elif selection == "10":
            text = input("Enter file path: ").strip()
            n = _ask_int("How many lines (default=10):? ", default=10, min_value=1)

            try:
                n =int(input("How many lines (default = 10):").strip() or "10")
            except :
                n =10
            head(text, n)
        elif selection == "11":
            text = input("Enter file path: ").strip()
            try:
                n=int(input("How many lines (default = 10):").strip() or "10")
            except :
                n = 10
        elif selection == "12":
            text = input("Enter file path: ").strip()
            undo_last_write(text)

        elif selection == "13" :
            print("Exiting...")
            break
        else:

            print("You have chosen an invalid number.")


# Programı çalıştıran ana blok

if __name__ == "__main__":
    menu()  # Menü başlat


