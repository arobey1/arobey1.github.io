import puz
import os
import sys
from datetime import datetime

def puz_to_text(puz_file, output_file=None):
    """Convert a .puz file to the text format for easy editing"""
    p = puz.read(puz_file)
    
    if not output_file:
        base_name = os.path.splitext(os.path.basename(puz_file))[0]
        output_file = f"{base_name}.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"TITLE: {p.title}\n")
        f.write(f"AUTHOR: {p.author}\n")
        
        # Try to extract date from filename
        puz_name = os.path.basename(puz_file)
        date_match = re.search(r"(\d{2})(\d{2})(\d{2})", puz_name)
        if date_match:
            yy, mm, dd = date_match.groups()
            f.write(f"DATE: 20{yy}-{mm}-{dd}\n")
        else:
            f.write("DATE: \n")
        
        f.write(f"COPYRIGHT: {p.copyright}\n")
        f.write("\n")
        f.write("GRID:\n")
        
        # Write grid
        for r in range(p.height):
            row = []
            for c in range(p.width):
                idx = r * p.width + c
                char = p.solution[idx]
                if char == '.':
                    row.append('.')
                else:
                    row.append(char)
            f.write("".join(row) + "\n")
        
        f.write("\n")
        f.write("ACROSS:\n")
        
        # Extract across clues
        across_clues = []
        down_clues = []
        
        # Calculate numbering to match clues
        def is_black(r, c):
            if r < 0 or r >= p.height or c < 0 or c >= p.width:
                return True
            idx = r * p.width + c
            return p.solution[idx] == '.'
        
        clue_num = 0
        clue_idx = 0
        
        for r in range(p.height):
            for c in range(p.width):
                if is_black(r, c):
                    continue
                
                can_go_across = (c + 1 < p.width) and not is_black(r, c+1)
                can_go_down = (r + 1 < p.height) and not is_black(r+1, c)
                
                is_across_start = is_black(r, c-1) and can_go_across
                is_down_start = is_black(r-1, c) and can_go_down
                
                if is_across_start or is_down_start:
                    clue_num += 1
                    if is_across_start:
                        if clue_idx < len(p.clues):
                            across_clues.append((clue_num, p.clues[clue_idx]))
                            clue_idx += 1
                    if is_down_start:
                        if clue_idx < len(p.clues):
                            down_clues.append((clue_num, p.clues[clue_idx]))
                            clue_idx += 1
        
        for num, clue in across_clues:
            f.write(f"{num}. {clue}\n")
        
        f.write("\n")
        f.write("DOWN:\n")
        
        for num, clue in down_clues:
            f.write(f"{num}. {clue}\n")
    
    print(f"Converted {puz_file} to {output_file}")
    print(f"Grid: {p.width}x{p.height}")
    print(f"Clues: {len(across_clues)} Across, {len(down_clues)} Down")

if __name__ == "__main__":
    import re
    
    if len(sys.argv) < 2:
        print("Usage: python puz_to_text.py <input.puz> [output.txt]")
        sys.exit(1)
    
    puz_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        puz_to_text(puz_file, output_file)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)



