import puz
import os
import re
from datetime import datetime

def sanitize_text(text):
    """Replace Unicode characters that can't be encoded in latin-1"""
    replacements = {
        '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '--',
        '\u2026': '...',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('iso-8859-1', 'replace').decode('iso-8859-1')

def parse_crossword_file(filepath):
    """Parse a simple text format crossword file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    metadata = {}
    grid_lines = []
    clues = {'across': [], 'down': []}
    mode = None
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # Parse metadata
        if line.upper().startswith('TITLE:'):
            metadata['title'] = line.split(':', 1)[1].strip()
        elif line.upper().startswith('AUTHOR:'):
            metadata['author'] = line.split(':', 1)[1].strip()
        elif line.upper().startswith('DATE:'):
            date_str = line.split(':', 1)[1].strip()
            metadata['date'] = date_str
        elif line.upper().startswith('COPYRIGHT:'):
            metadata['copyright'] = line.split(':', 1)[1].strip()
        elif line.upper() == 'GRID:':
            # Read grid lines until we hit a blank line or section header
            i += 1
            while i < len(lines):
                grid_line = lines[i].strip()
                if not grid_line or grid_line.upper() in ['ACROSS:', 'DOWN:']:
                    break
                grid_lines.append(grid_line)
                i += 1
            continue
        elif line.upper() == 'ACROSS:':
            mode = 'across'
        elif line.upper() == 'DOWN:':
            mode = 'down'
        elif mode and line:
            # Parse clue (format: "1. Clue text" or just "Clue text")
            clue_text = re.sub(r'^\d+\.\s*', '', line)
            clues[mode].append(sanitize_text(clue_text))
        
        i += 1
    
    return metadata, grid_lines, clues

def calculate_numbering(grid, cols, rows):
    """Calculate clue numbering based on grid structure"""
    numbering = []
    
    def is_black(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return True
        return grid[r][c] == '.'
    
    current_num = 0
    for r in range(rows):
        for c in range(cols):
            if is_black(r, c):
                continue
            
            can_go_across = (c + 1 < cols) and not is_black(r, c+1)
            can_go_down = (r + 1 < rows) and not is_black(r+1, c)
            
            is_across_start = is_black(r, c-1) and can_go_across
            is_down_start = is_black(r-1, c) and can_go_down
            
            if is_across_start or is_down_start:
                current_num += 1
                if is_across_start:
                    numbering.append({'num': current_num, 'dir': 'across'})
                if is_down_start:
                    numbering.append({'num': current_num, 'dir': 'down'})
    
    return numbering

def create_puz_from_text(text_file, output_file=None):
    """Convert a text format crossword file to .puz format"""
    metadata, grid_lines, clues = parse_crossword_file(text_file)
    
    if not grid_lines:
        raise ValueError("No grid found in file")
    
    rows = len(grid_lines)
    cols = max(len(line) for line in grid_lines) if grid_lines else 0
    
    # Normalize grid - pad shorter lines and convert to uppercase
    grid = []
    for line in grid_lines:
        # Pad line to full width
        padded = line.ljust(cols)
        # Convert to list of characters, normalize
        row = []
        for char in padded:
            if char == '.' or char == '#':
                row.append('.')
            elif char == '-' or char == ' ' or char == '_':
                row.append('?')  # Empty white cell
            else:
                row.append(char.upper())
        grid.append(row)
    
    # Create puzzle
    p = puz.Puzzle()
    p.width = cols
    p.height = rows
    
    # Build solution and fill strings
    sol_str = ""
    fill_str = ""
    for r in range(rows):
        for c in range(cols):
            char = grid[r][c]
            sol_str += char if char != '?' else 'X'
            fill_str += '.' if char == '.' else '-'
    
    p.solution = sol_str
    p.fill = fill_str
    
    # Calculate numbering
    numbering = calculate_numbering(grid, cols, rows)
    
    # Match clues to numbering
    sorted_clues = []
    across_idx = 0
    down_idx = 0
    
    for entry in numbering:
        if entry['dir'] == 'across':
            if across_idx < len(clues['across']):
                sorted_clues.append(clues['across'][across_idx])
                across_idx += 1
            else:
                sorted_clues.append(f"Missing Across Clue {entry['num']}")
        else:
            if down_idx < len(clues['down']):
                sorted_clues.append(clues['down'][down_idx])
                down_idx += 1
            else:
                sorted_clues.append(f"Missing Down Clue {entry['num']}")
    
    p.clues = sorted_clues
    
    # Set metadata
    p.title = metadata.get('title', 'Untitled Crossword')
    p.author = metadata.get('author', 'Unknown')
    p.copyright = metadata.get('copyright', '')
    
    # Generate output filename if not provided
    if not output_file:
        # Try to extract date from metadata or filename
        date_str = metadata.get('date', '')
        if date_str:
            # Parse date and format as cvYYMMDD.puz
            try:
                if '-' in date_str:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                else:
                    date_obj = datetime.strptime(date_str, '%Y/%m/%d')
                out_name = f"cv{date_obj.strftime('%y%m%d')}.puz"
            except:
                out_name = "puzzle.puz"
        else:
            out_name = "puzzle.puz"
        
        script_dir = os.path.dirname(os.path.abspath(text_file))
        output_file = os.path.join(script_dir, out_name)
    
    p.save(output_file)
    print(f"Saved to {output_file}")
    print(f"Grid: {cols}x{rows}")
    print(f"Clues: {len([n for n in numbering if n['dir']=='across'])} Across, {len([n for n in numbering if n['dir']=='down'])} Down")
    
    return output_file

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python convert_from_text.py <input.txt> [output.puz]")
        print("\nInput format:")
        print("TITLE: Crossword Title")
        print("AUTHOR: Author Name")
        print("DATE: 2016-04-26")
        print("COPYRIGHT: Copyright info")
        print("")
        print("GRID:")
        print("A..EF.EBSQT..F.")
        print(".A.RL.TLPA.A.ADA")
        print("...")
        print("")
        print("ACROSS:")
        print("1. First clue")
        print("2. Second clue")
        print("...")
        print("")
        print("DOWN:")
        print("1. First down clue")
        print("...")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        create_puz_from_text(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()


