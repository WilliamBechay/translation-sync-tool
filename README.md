# 🌍 Translation Sync Tool (script.py)

A Python GUI tool that automatically synchronizes all JSON translation files in a folder.  
The script detects missing keys based on the master English file, auto-translates them, and updates each translation file.

## 🚀 Features

- Clean and simple Tkinter GUI.
- Automatic detection of:
  - the master file (English: en.json, english.json, etc.)
  - all other translation files in the folder.
- Full JSON analysis:
  - key comparison,
  - missing key detection,
  - reconstruction of JSON structure.
- Automatic translation using GoogleTranslator (deep-translator).
- Clean file updates without modifying the master file.
- Real-time logging inside the interface.
- Runs in a separate thread to keep the UI responsive.

## 📦 Installation

### 1. Clone the project

git clone https://github.com/YOUR_REPO/translation-sync-tool
cd translation-sync-tool

### 2. Install dependencies

Create a `requirements.txt` with:

deep-translator
tk

Then install:

pip install -r requirements.txt

## ▶️ Run the program

python script.py

## 🧠 How it works

1. Open the interface.
2. Click "Browse" and select a folder containing `.json` translation files.
3. The script:
   - detects the master English file,
   - loads all other translations,
   - identifies missing keys,
   - auto-translates missing content,
   - rebuilds the proper JSON structure,
   - updates each translation file.

No application logic is modified — only translation files.

## 📂 Recommended file structure

translations/
├── en.json        ← master file
├── fr.json
├── es.json
├── ar.json
└── de.json

## ⚠️ Limitations

- Automatic translations may need manual review.
- The master file is never modified.