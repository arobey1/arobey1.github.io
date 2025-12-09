import cv2
import docx
import puz
import pytesseract
import numpy as np
import os
import re
from collections import defaultdict

def sanitize_text(text):
    replacements = {
        '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '--',
        '\u2026': '...',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('iso-8859-1', 'replace').decode('iso-8859-1')

def extract_clues(docx_path):
    doc = docx.Document(docx_path)
    clues = {'across': [], 'down': []}
    mode = None
    
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text: continue
        
        if text.upper() == 'ACROSS':
            mode = 'across'
            continue
        elif text.upper() == 'DOWN':
            mode = 'down'
            continue
            
        if mode:
            text = sanitize_text(text)
            clean_text = re.sub(r'^\d+\.\s*', '', text)
            clues[mode].append(clean_text)
            
    return clues

def find_grid_region(img, gray):
    """Try to find the actual crossword grid region, excluding UI elements"""
    # Use edge detection to find the grid
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours that might be the grid boundary
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Look for large rectangular contours
    for cnt in sorted(contours, key=cv2.contourArea, reverse=True)[:5]:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect = float(w) / h if h > 0 else 0
        
        # Grid should be roughly square-ish
        if 0.7 < aspect < 1.3 and w > 200 and h > 200:
            # Found potential grid region
            return (x, y, w, h)
    
    return None

def process_grid(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Failed to load image")
        return None, 0, 0
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Try to find grid region first
    grid_region = find_grid_region(img, gray)
    if grid_region:
        x, y, w, h = grid_region
        print(f"Found grid region at ({x}, {y}), size {w}x{h}")
        gray = gray[y:y+h, x:x+w]
        img = img[y:y+h, x:x+w]
    
    # Preprocess
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                    cv2.THRESH_BINARY, 11, 2)
    binary_inv = cv2.bitwise_not(binary)
    
    # Detect grid lines with morphological operations
    # Use smaller kernels for finer detection
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))
    
    h_lines = cv2.morphologyEx(binary_inv, cv2.MORPH_OPEN, h_kernel, iterations=1)
    v_lines = cv2.morphologyEx(binary_inv, cv2.MORPH_OPEN, v_kernel, iterations=1)
    
    # Projection profiles
    h_proj = np.sum(h_lines, axis=1)
    v_proj = np.sum(v_lines, axis=0)
    
    # More conservative peak detection
    h_thresh = np.max(h_proj) * 0.3  # Higher threshold
    v_thresh = np.max(v_proj) * 0.3
    
    def find_peaks(proj, thresh, min_dist=8):
        peaks = []
        i = 0
        while i < len(proj):
            if proj[i] > thresh:
                start = i
                peak_sum = proj[i]
                i += 1
                while i < len(proj) and proj[i] > thresh:
                    peak_sum += proj[i]
                    i += 1
                # Center of peak
                center = start + (i - start) // 2
                peaks.append(center)
                i += min_dist
            else:
                i += 1
        return peaks
    
    h_peaks = find_peaks(h_proj, h_thresh)
    v_peaks = find_peaks(v_proj, v_thresh)
    
    # Filter to remove duplicates
    def dedupe_peaks(peaks, min_dist=5):
        if not peaks: return []
        sorted_peaks = sorted(peaks)
        result = [sorted_peaks[0]]
        for p in sorted_peaks[1:]:
            if p - result[-1] >= min_dist:
                result.append(p)
        return result
    
    h_peaks = dedupe_peaks(h_peaks)
    v_peaks = dedupe_peaks(v_peaks)
    
    # Validate grid dimensions
    if len(h_peaks) < 3 or len(v_peaks) < 3:
        print("Not enough grid lines detected")
        return process_grid_contour_fallback(img, gray)
    
    rows = len(h_peaks) - 1
    cols = len(v_peaks) - 1
    
    # Snap to standard crossword sizes if close
    # Common sizes: 15x15, 21x21, 13x13, 17x17
    standard_sizes = [15, 21, 13, 17]
    
    # If one dimension is standard and the other is off by 1, correct it
    if rows in standard_sizes and abs(cols - rows) <= 1:
        cols = rows
        print(f"Correcting dimensions to {cols}x{rows} (standard size)")
        # Remove extra peak if needed
        if len(v_peaks) > len(h_peaks):
            # Remove the first or last peak (usually border artifact)
            if abs(v_peaks[0] - 0) < abs(v_peaks[-1] - gray.shape[1]):
                v_peaks = v_peaks[1:]
            else:
                v_peaks = v_peaks[:-1]
            cols = len(v_peaks) - 1
    elif cols in standard_sizes and abs(rows - cols) <= 1:
        rows = cols
        print(f"Correcting dimensions to {cols}x{rows} (standard size)")
        if len(h_peaks) > len(v_peaks):
            if abs(h_peaks[0] - 0) < abs(h_peaks[-1] - gray.shape[0]):
                h_peaks = h_peaks[1:]
            else:
                h_peaks = h_peaks[:-1]
            rows = len(h_peaks) - 1
    
    # Sanity check - typical crosswords are 15x15, 21x21, etc.
    # If way off, try alternative
    if rows > 25 or cols > 25 or rows < 5 or cols < 5:
        print(f"Grid dimensions {cols}x{rows} seem unreasonable, trying alternative...")
        return process_grid_contour_fallback(img, gray)
    
    print(f"Detected grid: {cols}x{rows} (from {len(h_peaks)} horizontal, {len(v_peaks)} vertical lines)")
    
    solution = [['.' for _ in range(cols)] for _ in range(rows)]
    custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    for r in range(rows):
        for c in range(cols):
            y1 = max(0, h_peaks[r])
            y2 = min(gray.shape[0], h_peaks[r+1])
            x1 = max(0, v_peaks[c])
            x2 = min(gray.shape[1], v_peaks[c+1])
            
            cell_roi = gray[y1:y2, x1:x2]
            
            if cell_roi.size == 0: 
                solution[r][c] = '.'
                continue
            
            mean_val = cv2.mean(cell_roi)[0]
            
            if mean_val < 130:  # Black cells
                solution[r][c] = '.'
            else:
                # White cell - OCR
                _, cell_thresh = cv2.threshold(cell_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                char = pytesseract.image_to_string(cell_thresh, config=custom_config)
                char = char.strip().upper()
                solution[r][c] = char[0] if char and char.isalpha() else '?'
                    
    return solution, cols, rows

def process_grid_contour_fallback(img, gray):
    """Fallback method using contour detection"""
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cells = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 100: continue
        
        x, y, w, h = cv2.boundingRect(cnt)
        aspect = float(w) / h if h > 0 else 0
        
        if 0.7 < aspect < 1.3 and 20 < w < 200 and 20 < h < 200:
            cells.append((x, y, w, h))
    
    if len(cells) < 10:
        print("Not enough cells found in fallback")
        return None, 0, 0
    
    # Cluster positions more aggressively
    x_coords = sorted(set([c[0] for c in cells]))
    y_coords = sorted(set([c[1] for c in cells]))
    
    def cluster(coords, tol=20):
        clusters = []
        for coord in coords:
            found = False
            for cluster in clusters:
                if abs(coord - np.mean(cluster)) < tol:
                    cluster.append(coord)
                    found = True
                    break
            if not found:
                clusters.append([coord])
        return sorted([int(np.median(c)) for c in clusters])
    
    x_clustered = cluster(x_coords, tol=25)
    y_clustered = cluster(y_coords, tol=25)
    
    cols = len(x_clustered)
    rows = len(y_clustered)
    
    print(f"Fallback detection: {cols}x{rows}")
    
    solution = [['.' for _ in range(cols)] for _ in range(rows)]
    cell_map = {}
    
    for (x, y, w, h) in cells:
        c = min(range(cols), key=lambda i: abs(x - x_clustered[i]))
        r = min(range(rows), key=lambda i: abs(y - y_clustered[i]))
        cell_map[(r, c)] = (x, y, w, h)
    
    custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) in cell_map:
                (x, y, w, h) = cell_map[(r, c)]
                pad = max(2, int(min(w, h) * 0.1))
                roi = gray[y+pad:y+h-pad, x+pad:x+w-pad]
                
                if roi.size == 0:
                    solution[r][c] = '.'
                    continue
                    
                mean_val = cv2.mean(roi)[0]
                if mean_val < 130:
                    solution[r][c] = '.'
                else:
                    _, cell_thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    char = pytesseract.image_to_string(cell_thresh, config=custom_config)
                    char = char.strip().upper()
                    solution[r][c] = char[0] if char and char.isalpha() else '?'
            else:
                solution[r][c] = '.'
    
    return solution, cols, rows

def calculate_numbering(grid, cols, rows):
    numbering = []
    
    def is_black(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols: return True
        return grid[r][c] == '.'

    current_num = 0
    for r in range(rows):
        for c in range(cols):
            if is_black(r, c): continue
            
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

def create_puz(clues, grid, cols, rows, output_path):
    p = puz.Puzzle()
    p.width = cols
    p.height = rows
    
    sol_str = ""
    fill_str = ""
    for r in range(rows):
        for c in range(cols):
            char = grid[r][c]
            sol_str += char if char != '?' else 'X'
            fill_str += '.' if char == '.' else '-'
            
    p.solution = sol_str
    p.fill = fill_str
    
    numbering = calculate_numbering(grid, cols, rows)
    
    print(f"Calculated numbering: {len([n for n in numbering if n['dir']=='across'])} Across, {len([n for n in numbering if n['dir']=='down'])} Down")
    print(f"Available clues: {len(clues['across'])} Across, {len(clues['down'])} Down")
    
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
    p.title = "Crossword 9"
    p.author = "Unknown"
    p.copyright = "Unknown"
    
    p.save(output_path)
    print(f"Saved to {output_path}")
    
    # Print grid for verification
    print("\nGrid structure:")
    for r in range(rows):
        print("".join(grid[r]))

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docx_path = os.path.join(script_dir, "Crossword9.docx")
    img_path = os.path.join(script_dir, "Screen Shot 2016-04-26 at 9.48.47 PM.png")
    
    print("Extracting clues...")
    clues = extract_clues(docx_path)
    print(f"Found {len(clues['across'])} Across, {len(clues['down'])} Down.")
    
    print("Processing grid...")
    grid, cols, rows = process_grid(img_path)
    if not grid: return
    
    # Extract date from image filename
    img_filename = os.path.basename(img_path)
    date_match = re.search(r"(\d{4})-(\d{2})-(\d{2})", img_filename)
    if date_match:
        y, m, d = date_match.groups()
        out_name = f"cv{y[2:]}{m}{d}.puz"
    else:
        out_name = "puzzle.puz"
    
    output = os.path.join(script_dir, out_name)
    create_puz(clues, grid, cols, rows, output)

if __name__ == "__main__":
    main()
