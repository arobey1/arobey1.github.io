#!/usr/bin/env python3
"""
Script to add a new crossword puzzle to puzzles.json

Usage:
    python add_puzzle.py <puzzle_file.puz> [puzzles.json]

Examples:
    python add_puzzle.py nyt251129.puz
    python add_puzzle.py new_puzzle.puz puzzles.json

Note: This script requires the 'puz' library. If you get a ModuleNotFoundError,
      activate the virtual environment first:
      source converter/venv/bin/activate
      python add_puzzle.py <puzzle_file.puz>
"""

import json
import os
import re
import sys
from datetime import datetime

try:
    import puz
except ImportError:
    print("Error: 'puz' module not found.")
    print("\nTo fix this, activate the virtual environment:")
    print("  source converter/venv/bin/activate")
    print("\nOr use the wrapper script:")
    print("  ./add_puzzle.sh <puzzle_file.puz>")
    sys.exit(1)

def extract_puzzle_info(puz_file):
    """Extract puzzle information from a .puz file"""
    p = puz.read(puz_file)
    
    # Extract date from filename (format: nyt251129.puz -> 2025-11-29)
    filename = os.path.basename(puz_file)
    date_match = re.search(r"(\d{2})(\d{2})(\d{2})", filename)
    if date_match:
        yy, mm, dd = date_match.groups()
        date_str = f"20{yy}-{mm}-{dd}"
    else:
        date_str = ""
        print(f"Warning: Could not extract date from filename '{filename}'. Date will be empty.")
    
    # Convert grid to flattened array (0 = black, 1 = white)
    grid = []
    for r in range(p.height):
        for c in range(p.width):
            idx = r * p.width + c
            char = p.solution[idx]
            # 0 for black (.), 1 for white (letter)
            grid.append(0 if char == '.' else 1)
    
    return {
        "filename": filename,
        "title": p.title,
        "author": p.author,
        "width": p.width,
        "height": p.height,
        "grid": grid,
        "date": date_str
    }

def add_puzzle_to_json(puz_file, json_file):
    """Add puzzle info to puzzles.json"""
    # Read existing puzzles
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            puzzles = json.load(f)
    else:
        puzzles = []
        print(f"Creating new {json_file}")
    
    # Extract new puzzle info
    print(f"Parsing puzzle: {puz_file}")
    new_puzzle = extract_puzzle_info(puz_file)
    
    # Move puzzle file to puzzles/ subfolder if it's not already there
    script_dir = os.path.dirname(os.path.abspath(json_file))
    puzzles_dir = os.path.join(script_dir, 'puzzles')
    source_path = puz_file if os.path.isabs(puz_file) else os.path.join(script_dir, puz_file)
    dest_path = os.path.join(puzzles_dir, new_puzzle['filename'])
    
    # Create puzzles directory if it doesn't exist
    if not os.path.exists(puzzles_dir):
        os.makedirs(puzzles_dir)
        print(f"Created puzzles directory: {puzzles_dir}")
    
    # Move file if it's not already in the puzzles folder
    if os.path.abspath(source_path) != os.path.abspath(dest_path):
        if os.path.exists(source_path):
            import shutil
            shutil.move(source_path, dest_path)
            print(f"Moved puzzle file to: {dest_path}")
        elif not os.path.exists(dest_path):
            print(f"Warning: Source file {source_path} not found, and destination {dest_path} doesn't exist.")
    
    # Check if puzzle already exists
    existing_filenames = [p['filename'] for p in puzzles]
    if new_puzzle['filename'] in existing_filenames:
        print(f"\nError: Puzzle '{new_puzzle['filename']}' already exists in {json_file}")
        print(f"  Title: {new_puzzle['title']}")
        print(f"  Author: {new_puzzle['author']}")
        response = input("\nDo you want to replace it? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            # Remove existing puzzle
            puzzles = [p for p in puzzles if p['filename'] != new_puzzle['filename']]
            print("Removed existing puzzle.")
        else:
            print("Cancelled. No changes made.")
            return False
    
    # Add new puzzle (prepend to keep newest first)
    puzzles.insert(0, new_puzzle)
    
    # Write back to JSON
    with open(json_file, 'w') as f:
        json.dump(puzzles, f)
    
    print(f"\n✓ Successfully added puzzle:")
    print(f"  Title: {new_puzzle['title']}")
    print(f"  Author: {new_puzzle['author']}")
    print(f"  Date: {new_puzzle['date']}")
    print(f"  Size: {new_puzzle['width']}x{new_puzzle['height']}")
    print(f"  File: {new_puzzle['filename']}")
    print(f"\nTotal puzzles in archive: {len(puzzles)}")
    return True

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    puz_file = sys.argv[1]
    json_file = sys.argv[2] if len(sys.argv) > 2 else "puzzles.json"
    
    # Resolve paths relative to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    puz_path = os.path.join(script_dir, puz_file) if not os.path.isabs(puz_file) else puz_file
    json_path = os.path.join(script_dir, json_file) if not os.path.isabs(json_file) else json_file
    
    if not os.path.exists(puz_path):
        print(f"Error: File '{puz_file}' not found")
        print(f"  Looked for: {puz_path}")
        sys.exit(1)
    
    try:
        success = add_puzzle_to_json(puz_path, json_path)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

