import cv2
import numpy as np
import os
import sys
import re

def extract_grid_structure(image_path, output_file=None):
    """
    Extract the grid structure from an image and output as text format.
    This creates a template that you can manually edit and verify.
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load image: {image_path}")
        return
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Simple thresholding
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    binary_inv = cv2.bitwise_not(binary)
    
    # Detect grid lines
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))
    
    h_lines = cv2.morphologyEx(binary_inv, cv2.MORPH_OPEN, h_kernel, iterations=1)
    v_lines = cv2.morphologyEx(binary_inv, cv2.MORPH_OPEN, v_kernel, iterations=1)
    
    h_proj = np.sum(h_lines, axis=1)
    v_proj = np.sum(v_lines, axis=0)
    
    h_thresh = np.max(h_proj) * 0.3
    v_thresh = np.max(v_proj) * 0.3
    
    def find_peaks(proj, thresh, min_dist=8):
        peaks = []
        i = 0
        while i < len(proj):
            if proj[i] > thresh:
                start = i
                i += 1
                while i < len(proj) and proj[i] > thresh:
                    i += 1
                center = start + (i - start) // 2
                peaks.append(center)
                i += min_dist
            else:
                i += 1
        return peaks
    
    h_peaks = sorted(find_peaks(h_proj, h_thresh))
    v_peaks = sorted(find_peaks(v_proj, v_thresh))
    
    # Remove duplicates
    def dedupe(peaks, min_dist=5):
        if not peaks: return []
        result = [peaks[0]]
        for p in peaks[1:]:
            if p - result[-1] >= min_dist:
                result.append(p)
        return result
    
    h_peaks = dedupe(h_peaks)
    v_peaks = dedupe(v_peaks)
    
    # Snap to standard size if close
    rows = len(h_peaks) - 1
    cols = len(v_peaks) - 1
    
    standard_sizes = [15, 21, 13, 17]
    if rows in standard_sizes and abs(cols - rows) <= 1:
        cols = rows
        if len(v_peaks) > len(h_peaks):
            v_peaks = v_peaks[:len(h_peaks)]
    
    rows = len(h_peaks) - 1
    cols = len(v_peaks) - 1
    
    print(f"Detected grid: {cols}x{rows}")
    
    # Extract grid
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            y1 = max(0, h_peaks[r])
            y2 = min(gray.shape[0], h_peaks[r+1])
            x1 = max(0, v_peaks[c])
            x2 = min(gray.shape[1], v_peaks[c+1])
            
            cell_roi = gray[y1:y2, x1:x2]
            if cell_roi.size == 0:
                row.append('.')
                continue
            
            mean_val = cv2.mean(cell_roi)[0]
            
            if mean_val < 130:
                row.append('.')  # Black cell
            else:
                # Try to detect if there's a letter
                # For now, mark as empty white cell
                row.append('?')
        grid.append(row)
    
    # Generate output filename
    if not output_file:
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_file = f"{base_name}_grid.txt"
    
    # Write template file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("TITLE: Crossword\n")
        f.write("AUTHOR: Unknown\n")
        
        # Try to extract date from filename
        img_name = os.path.basename(image_path)
        date_match = re.search(r"(\d{4})-(\d{2})-(\d{2})", img_name)
        if date_match:
            y, m, d = date_match.groups()
            f.write(f"DATE: {y}-{m}-{d}\n")
        else:
            f.write("DATE: \n")
        
        f.write("COPYRIGHT: \n")
        f.write("\n")
        f.write("GRID:\n")
        
        for row in grid:
            f.write("".join(row) + "\n")
        
        f.write("\n")
        f.write("ACROSS:\n")
        f.write("1. [Edit clues here]\n")
        f.write("2. \n")
        f.write("...\n")
        f.write("\n")
        f.write("DOWN:\n")
        f.write("1. [Edit clues here]\n")
        f.write("2. \n")
        f.write("...\n")
    
    print(f"Created template file: {output_file}")
    print("\nNext steps:")
    print("1. Open the template file and verify/correct the grid structure")
    print("2. Replace '?' with actual letters from the image")
    print("3. Add the clues from your Word document")
    print("4. Run: python convert_from_text.py <template_file>")

if __name__ == "__main__":
    import re
    
    if len(sys.argv) < 2:
        print("Usage: python extract_grid.py <image.png> [output.txt]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    extract_grid_structure(image_path, output_file)

