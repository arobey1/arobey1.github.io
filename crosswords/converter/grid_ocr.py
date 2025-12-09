import cv2
import numpy as np
import sys
import os
import pytesseract

def process_grid(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Failed to load image")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Invert for contour detection
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    squares = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w)/h
            # Filter for cell-sized squares
            if 0.8 < aspect_ratio < 1.2 and w > 20 and h > 20:
                squares.append((x, y, w, h))
    
    if not squares:
        print("No squares found")
        return None

    # Robust Grid Estimation
    min_x = min(s[0] for s in squares)
    min_y = min(s[1] for s in squares)
    
    # Use median size
    med_w = np.median([s[2] for s in squares])
    med_h = np.median([s[3] for s in squares])
    
    # Snap coords to grid
    cells = {}
    max_c = 0
    max_r = 0
    
    for (x, y, w, h) in squares:
        c = round((x - min_x) / med_w)
        r = round((y - min_y) / med_h)
        max_c = max(max_c, c)
        max_r = max(max_r, r)
        cells[(r, c)] = (x, y, w, h)
        
    cols = max_c + 1
    rows = max_r + 1
    
    print(f"Grid dimensions: {cols}x{rows}")
    
    # Create solution grid
    # Initialize with '.' (black)
    solution = [['.' for _ in range(cols)] for _ in range(rows)]
    
    # Configuration for single character
    custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) in cells:
                # It's a cell. Is it black or white?
                # Check brightness of center
                (x, y, w, h) = cells[(r, c)]
                
                # Inner crop
                pad = int(w * 0.15)
                roi = gray[y+pad:y+h-pad, x+pad:x+w-pad]
                
                if roi.size == 0: continue
                
                mean_val = cv2.mean(roi)[0]
                
                if mean_val < 100:
                    # Black cell
                    solution[r][c] = '.'
                else:
                    # White cell - OCR it
                    # Use original (not inverted) roi for OCR, maybe binarize
                    _, cell_thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    
                    # Tesseract on this small patch
                    char = pytesseract.image_to_string(cell_thresh, config=custom_config)
                    char = char.strip().upper()
                    
                    if char and char.isalpha():
                        solution[r][c] = char[0]
                    else:
                        solution[r][c] = '?' # Unknown/Empty
                        
    return solution

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "Screen Shot 2016-04-26 at 9.48.47 PM.png")
    grid = process_grid(img_path)
    
    if grid:
        for row in grid:
            print("".join(row))


