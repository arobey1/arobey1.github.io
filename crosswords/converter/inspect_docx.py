import docx
import sys
import os

def inspect_docx(filename):
    # resolve path relative to this script if needed
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, filename)
    
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        return

    print(f"Reading {full_path}...")
    doc = docx.Document(full_path)
    print("Paragraphs:")
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if text:
            print(f"{i}: {text}")

if __name__ == "__main__":
    inspect_docx("Crossword9.docx")
