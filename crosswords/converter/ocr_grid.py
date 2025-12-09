import cv2
import pytesseract
from pytesseract import Output
import os
import numpy as np

def ocr_grid(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Get data with bounding boxes
    # config: assume single character per box? No, standard.
    # psm 6: Assume a single uniform block of text.
    # psm 11: Sparse text.
    # psm 12: Sparse text with OSD.
    
    # We want to detect letters.
    # Let's try default.
    data = pytesseract.image_to_data(gray, output_type=Output.DICT, config='--psm 6')
    
    boxes = []
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        text = data['text'][i].strip()
        if not text: continue
        if len(text) > 1: 
            # If it detected a word, split it roughly? 
            # Or assume it's a single char per cell and tesseract merged them?
            pass
            
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        # Filter huge or tiny things
        if h < 10: continue
        
        boxes.append({
            'text': text,
            'x': x, 'y': y, 'w': w, 'h': h
        })
        
    print(f"Detected {len(boxes)} text elements.")
    
    # Determine Grid Geometry from boxes
    if not boxes:
        return

    # Center points
    cx = [b['x'] + b['w']/2 for b in boxes]
    cy = [b['y'] + b['h']/2 for b in boxes]
    
    # Infer spacing
    # Sort by x, find diffs
    cx_sorted = sorted(cx)
    cy_sorted = sorted(cy)
    
    # Simple diffs
    diffs_x = np.diff(cx_sorted)
    diffs_y = np.diff(cy_sorted)
    
    # Filter small diffs (same col/row)
    spacings_x = [d for d in diffs_x if d > 10]
    spacings_y = [d for d in diffs_y if d > 10]
    
    if spacings_x:
        median_spacing_x = np.median(spacings_x)
        print(f"Median X spacing: {median_spacing_x}")
    if spacings_y:
        median_spacing_y = np.median(spacings_y)
        print(f"Median Y spacing: {median_spacing_y}")
        
    # Determine bounds
    min_x = min(b['x'] for b in boxes)
    max_x = max(b['x'] + b['w'] for b in boxes)
    min_y = min(b['y'] for b in boxes)
    max_y = max(b['y'] + b['h'] for b in boxes)
    
    # Estimate grid size
    # Assume median spacing is cell size roughly
    cell_size = (median_spacing_x + median_spacing_y) / 2
    
    cols = round((max_x - min_x) / cell_size) + 1
    rows = round((max_y - min_y) / cell_size) + 1
    
    print(f"Estimated Grid from Letters: {cols} x {rows}")
    
    # Build grid
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    
    for b in boxes:
        c = round((b['x'] + b['w']/2 - min_x) / cell_size)
        r = round((b['y'] + b['h']/2 - min_y) / cell_size)
        
        if 0 <= r < rows and 0 <= c < cols:
            # Take first char only
            char = b['text'][0].upper()
            if char.isalpha():
                grid[r][c] = char
            else:
                # Maybe a number?
                pass
                
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "Screen Shot 2016-04-26 at 9.48.47 PM.png")
    ocr_grid(img_path)


