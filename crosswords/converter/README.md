# Crossword Converter

This directory contains tools to convert crossword puzzles into `.puz` format.

## New Text-Based Workflow (Recommended)

Instead of trying to automatically detect everything from images, you can now use a simple text format that's easy to edit and verify.

### Step 1: Extract Grid Structure (Optional)

If you have an image of the completed grid, you can extract the structure:

```bash
python extract_grid.py "Screen Shot 2016-04-26 at 9.48.47 PM.png"
```

This creates a template file with the detected grid structure. You'll need to:
- Verify the grid dimensions are correct
- Replace `?` with actual letters from the image
- Replace `.` with `.` for black cells (these should already be correct)

### Step 2: Create/Edit Text File

Create a text file (or edit the template) with this format:

```
TITLE: Crossword Title
AUTHOR: Author Name
DATE: 2016-04-26
COPYRIGHT: Copyright info (optional)

GRID:
A..EF.EBSQT..F.
.A.RL.TLPA.A.ADA
.NARMRLDALEL.PLP
PSB...AE....A.ES
ESL..MLREE.AVL..
.HO.D...SE.PELSS
....S..ATEUP.SAR
C.LE.K.DGND..LDA
AOU.MELAP..AY...
.ADPLN.S...SER.P
..PSD.BHE.RM..OW
SBCT....SES..E.A
R.R.CRBCFTHBWLEK
.N..RAHLSA..ARRE
ETS.EALELS.FRLSS

ACROSS:
1. First across clue
2. Second across clue
3. Third across clue
...

DOWN:
1. First down clue
2. Second down clue
3. Third down clue
...
```

**Grid Format:**
- `.` = black cell (blocked)
- Letter = filled white cell
- `?` or `-` or `_` = empty white cell (will be converted to `-` in the puzzle)

**Clues Format:**
- Number prefix (e.g., "1. ") is optional - it will be stripped automatically
- Clues are matched to grid numbering automatically

### Step 3: Convert to .puz

```bash
python convert_from_text.py crossword.txt [output.puz]
```

If you don't specify an output file, it will generate one based on the date (e.g., `cv160426.puz`).

## Old Image-Based Workflow (Less Reliable)

The original `convert_to_puz.py` script attempts to automatically extract everything from a Word document and image, but the grid detection isn't always accurate. You can still use it, but you'll likely need to manually verify and correct the output.

## Tips

1. **Grid Structure**: Make sure each row has the same number of characters. The script will pad shorter rows automatically.

2. **Verification**: After conversion, open the `.puz` file in a crossword editor to verify the grid and clues are correct.

3. **Clue Ordering**: The script automatically calculates clue numbering based on the grid structure, so you just need to list clues in order (across first, then down).

4. **Template File**: See `crossword_template.txt` for a complete example.


