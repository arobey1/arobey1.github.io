import cv2
import numpy as np
import sys
import os

def detect_grid(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Failed to load image")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Thresholding to get black grid lines on white
    # Invert so lines are white on black for contour detection
    # Usually screenshots are white background, black text/lines.
    # Binary inv: 
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours that look like cells
    squares = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w)/h
            if 0.8 < aspect_ratio < 1.2 and w > 10 and h > 10:
                squares.append((x, y, w, h))
                
    print(f"Found {len(squares)} potential cell contours.")
    
    if not squares:
        return

    # Determine grid dimensions
    # Sort by y then x
    squares.sort(key=lambda s: (s[1] // 10, s[0])) # Bin y by 10px to handle slight misalignment
    
    # Infer rows and cols
    # We can look at the distinct x and y coordinates
    xs = sorted([s[0] for s in squares])
    ys = sorted([s[1] for s in squares])
    
    # Cluster them?
    # Simplest approach: assume the bounding box of all squares defines the grid area
    min_x = min(s[0] for s in squares)
    min_y = min(s[1] for s in squares)
    max_x = max(s[0] + s[2] for s in squares)
    max_y = max(s[1] + s[3] for s in squares)
    
    # Median cell size
    med_w = np.median([s[2] for s in squares])
    med_h = np.median([s[3] for s in squares])
    
    cols = round((max_x - min_x) / med_w)
    rows = round((max_y - min_y) / med_h)
    
    print(f"Estimated Grid: {cols} x {rows}")
    print(f"Median Cell Size: {med_w} x {med_h}")
    
    # Construct grid
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    
    # Map squares to grid coords
    for (x, y, w, h) in squares:
        c = round((x - min_x) / med_w)
        r = round((y - min_y) / med_h)
        if 0 <= c < cols and 0 <= r < rows:
            # If a square contour exists, it's likely a white cell (or black cell with border?)
            # Actually, in a screenshot, black cells are usually solid black.
            # If they are solid black, findContours on BINARY_INV might see them as solid blobs.
            # But if they have white borders?
            
            # Check average brightness of the internal area in original gray image
            # Crop slightly inside
            pad = int(w * 0.2)
            roi = gray[y+pad:y+h-pad, x+pad:x+w-pad]
            mean_val = cv2.mean(roi)[0]
            
            # White is 255, Black is 0.
            if mean_val < 100:
                grid[r][c] = '.' # Black
            else:
                grid[r][c] = 'X' # White (Solution holder)
                
    # Print grid
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "Screen Shot 2016-04-26 at 9.48.47 PM.png")
    detect_grid(img_path)


