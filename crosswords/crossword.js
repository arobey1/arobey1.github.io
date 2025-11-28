document.addEventListener('DOMContentLoaded', () => {
    loadPuzzle('uc251127.puz');
});

let puzzle = null;
let gameState = {
    grid: [], // 2D array of cell states
    cursor: { row: 0, col: 0 },
    direction: 'across', // 'across' or 'down'
    width: 0,
    height: 0
};

async function loadPuzzle(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Failed to load puzzle: ${response.statusText}`);
        const buffer = await response.arrayBuffer();
        puzzle = parsePuz(buffer);
        initGame();
    } catch (e) {
        console.error(e);
        document.getElementById('puzzle-title').textContent = "Error loading puzzle";
    }
}

function parsePuz(buffer) {
    const view = new DataView(buffer);
    const decoder = new TextDecoder('iso-8859-1');

    // Header parsing
    const width = view.getUint8(0x2C);
    const height = view.getUint8(0x2D);
    const numClues = view.getUint16(0x2E, true); // Little endian

    let offset = 0x34;
    
    // Solution
    const solution = decoder.decode(buffer.slice(offset, offset + width * height));
    offset += width * height;

    // Player state (ignored usually, but we can see if it's filled)
    // const playerState = decoder.decode(buffer.slice(offset, offset + width * height));
    offset += width * height;

    // Strings
    // Read until end of buffer, then split by null bytes
    const stringBytes = new Uint8Array(buffer.slice(offset));
    let stringData = decoder.decode(stringBytes);
    let strings = stringData.split('\0');

    const title = strings[0];
    const author = strings[1];
    const copyright = strings[2];
    
    // Clues
    // Filter out empty strings if any (sometimes there are extra nulls at end)
    const cluesList = strings.slice(3, 3 + numClues);
    
    // Parse grid to assign numbers and map clues
    const grid = [];
    let clueIndex = 0;
    const acrossClues = {};
    const downClues = {};
    
    let cellNumber = 1;
    
    for (let r = 0; r < height; r++) {
        const row = [];
        for (let c = 0; c < width; c++) {
            const idx = r * width + c;
            const char = solution[idx];
            const isBlack = char === '.';
            
            let number = null;
            let isAcrossStart = false;
            let isDownStart = false;

            if (!isBlack) {
                // Determine if this cell starts a word
                const leftBlack = c === 0 || solution[r * width + (c - 1)] === '.';
                const topBlack = r === 0 || solution[(r - 1) * width + c] === '.';
                
                if (leftBlack) {
                    isAcrossStart = true; 
                }
                
                if (topBlack) {
                     isDownStart = true;
                }
                
                if (isAcrossStart || isDownStart) {
                    number = cellNumber++;
                }
                
                if (isAcrossStart) {
                     if (clueIndex < cluesList.length) {
                         acrossClues[number] = cluesList[clueIndex++];
                     }
                }
                
                if (isDownStart) {
                    if (clueIndex < cluesList.length) {
                         downClues[number] = cluesList[clueIndex++];
                    }
                }
            }
            
            row.push({
                solution: char,
                isBlack: isBlack,
                number: number,
                userVal: '' // Start empty
            });
        }
        grid.push(row);
    }

    return {
        width,
        height,
        title,
        author,
        copyright,
        grid,
        acrossClues,
        downClues
    };
}

function initGame() {
    gameState.width = puzzle.width;
    gameState.height = puzzle.height;
    gameState.isSolved = false;
    // Init empty grid state
    gameState.grid = puzzle.grid.map(row => row.map(cell => ({ ...cell, userVal: '' })));
    
    // Find first non-black cell for initial cursor
    let found = false;
    for (let r=0; r<puzzle.height; r++) {
        for (let c=0; c<puzzle.width; c++) {
            if (!puzzle.grid[r][c].isBlack) {
                gameState.cursor = { row: r, col: c };
                found = true;
                break;
            }
        }
        if (found) break;
    }

    renderStaticElements();
    renderGrid(); // Just creates elements
    renderCluesList();
    updateUI();
    
    // Attach global event listeners
    document.addEventListener('keydown', handleKeydown);
    
    // Toolbar buttons
    document.getElementById('btn-clear-word').addEventListener('click', () => clearWord());
    document.getElementById('btn-clear-puzzle').addEventListener('click', () => clearPuzzle());
    document.getElementById('btn-reveal-cell').addEventListener('click', () => revealCell());
    document.getElementById('btn-reveal-word').addEventListener('click', () => revealWord());
    document.getElementById('btn-reveal-puzzle').addEventListener('click', () => revealPuzzle());
    document.getElementById('btn-check-cell').addEventListener('click', () => checkCell());
    document.getElementById('btn-check-word').addEventListener('click', () => checkWord());
    document.getElementById('btn-check-puzzle').addEventListener('click', () => checkPuzzle());
    document.getElementById('btn-rebus').addEventListener('click', () => startRebusMode());
    document.getElementById('btn-view-solved').addEventListener('click', () => {
        document.getElementById('success-modal').classList.remove('active');
        // Mark as solved so typing is disabled
        gameState.isSolved = true; 
    });
    
    // Rebus input listener
    const rebusInput = document.getElementById('rebus-input');
    rebusInput.addEventListener('keydown', (e) => handleRebusKeydown(e));
    rebusInput.addEventListener('blur', () => endRebusMode(false)); // Save on click away? Or cancel? Usually save.
}

function checkCompletion() {
    if (gameState.isSolved) return;
    
    let isComplete = true;
    let isCorrect = true;
    
    for(let r=0; r<puzzle.height; r++) {
        for(let c=0; c<puzzle.width; c++) {
            if (!gameState.grid[r][c].isBlack) {
                if (gameState.grid[r][c].userVal === '') {
                    isComplete = false;
                } else if (gameState.grid[r][c].userVal !== gameState.grid[r][c].solution) {
                    isCorrect = false;
                }
            }
        }
    }
    
    if (isComplete && isCorrect) {
        gameState.isSolved = true;
        // Show success modal
        setTimeout(() => {
             document.getElementById('success-modal').classList.add('active');
        }, 500);
    }
}

// --- Toolbar Functions ---

let isRebusMode = false;

function startRebusMode() {
    const { row, col } = gameState.cursor;
    if (gameState.grid[row][col].isBlack || gameState.grid[row][col].isRevealed || gameState.isSolved) return;
    
    isRebusMode = true;
    
    // Position overlay over the current cell
    const cell = document.getElementById(`cell-${row}-${col}`);
    const overlay = document.getElementById('rebus-overlay');
    const input = document.getElementById('rebus-input');
    
    const rect = cell.getBoundingClientRect();
    // Get container offset to position absolute correctly relative to .puzzle-area or body?
    // .puzzle-area has position? No.
    // We should likely append overlay to body or position fixed.
    // Or position absolute relative to grid-container.
    // Let's use fixed to be safe with transforms.
    
    // Actually, let's calculate relative to page
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
    
    overlay.style.position = 'absolute';
    overlay.style.top = (rect.top + scrollTop - 10) + 'px'; // Slightly larger/offset
    overlay.style.left = (rect.left + scrollLeft - 35) + 'px'; // Wider input
    overlay.style.width = (rect.width + 70) + 'px'; 
    overlay.style.height = (rect.height + 20) + 'px';
    overlay.style.display = 'flex';
    
    input.value = gameState.grid[row][col].userVal;
    input.focus();
}

function endRebusMode(save = true) {
    if (!isRebusMode) return;
    
    const input = document.getElementById('rebus-input');
    const overlay = document.getElementById('rebus-overlay');
    
    if (save) {
        const { row, col } = gameState.cursor;
        gameState.grid[row][col].userVal = input.value.toUpperCase();
        const el = document.getElementById(`cell-${row}-${col}`);
        if (el) el.classList.remove('wrong');
        
        // Move to next logical spot after Rebus entry
        const wordCells = getWordCells(row, col, gameState.direction);
        let currentIndex = -1;
        for(let i=0; i<wordCells.length; i++) {
            if (wordCells[i].r === row && wordCells[i].c === col) {
                currentIndex = i;
                break;
            }
        }
        
        // Search forward for next empty cell
        let targetIndex = -1;
        if (currentIndex !== -1) {
            for(let i = currentIndex + 1; i < wordCells.length; i++) {
                const c = wordCells[i];
                if (gameState.grid[c.r][c.c].userVal === '') {
                    targetIndex = i;
                    break;
                }
            }
        }
        
        // If not found forward, search from start (0) up to current
        if (targetIndex === -1) {
             for(let i = 0; i < currentIndex; i++) {
                const c = wordCells[i];
                if (gameState.grid[c.r][c.c].userVal === '') {
                    targetIndex = i;
                    break;
                }
            }
        }

        if (targetIndex !== -1) {
            const target = wordCells[targetIndex];
            gameState.cursor = { row: target.r, col: target.c };
        } else {
            // Word is full -> Move to next clue
            moveToNextLogicalClue(true);
        }
        
        updateUI();
        checkCompletion();
    }
    
    input.value = '';
    overlay.style.display = 'none';
    isRebusMode = false;
}

function handleRebusKeydown(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        endRebusMode(true);
    } else if (e.key === 'Escape') {
        e.preventDefault();
        endRebusMode(false); // Cancel
    }
    e.stopPropagation(); // Stop event from bubbling to game
}

function enterRebus() {
    // Deprecated in favor of startRebusMode
    startRebusMode();
}

function clearWord() {
    const { row, col } = gameState.cursor;
    const wordCells = getWordCells(row, col, gameState.direction);
    wordCells.forEach(({r, c}) => {
        gameState.grid[r][c].userVal = '';
        gameState.grid[r][c].isRevealed = false;
        gameState.grid[r][c].isRevealedByCheat = false;
        
        // Remove marks
        const el = document.getElementById(`cell-${r}-${c}`);
        if (el) el.classList.remove('wrong', 'revealed', 'checked-correct');
    });
    // If clearing a word, we're definitely not solved anymore (if we were)
    // But wait, if we clear, we want to be able to play again.
    if (gameState.isSolved) {
        gameState.isSolved = false;
    }
    updateUI();
}

function clearPuzzle() {
    if(!confirm("Are you sure you want to clear the entire puzzle?")) return;
    for(let r=0; r<puzzle.height; r++) {
        for(let c=0; c<puzzle.width; c++) {
            gameState.grid[r][c].userVal = '';
            gameState.grid[r][c].isRevealed = false;
            gameState.grid[r][c].isRevealedByCheat = false;
            
             const el = document.getElementById(`cell-${r}-${c}`);
             if (el) el.classList.remove('wrong', 'revealed', 'checked-correct');
        }
    }
    gameState.isSolved = false;
    updateUI();
}

function revealCell() {
    const { row, col } = gameState.cursor;
    if (gameState.grid[row][col].isBlack) return;
    
    gameState.grid[row][col].userVal = gameState.grid[row][col].solution;
    gameState.grid[row][col].isRevealed = true;
    gameState.grid[row][col].isRevealedByCheat = true; // Flag for red marker
    
    const el = document.getElementById(`cell-${row}-${col}`);
    if(el) {
        el.classList.remove('wrong');
        el.classList.add('revealed');
    }
    updateUI();
    checkCompletion();
}

function revealWord() {
    const { row, col } = gameState.cursor;
    const wordCells = getWordCells(row, col, gameState.direction);
    wordCells.forEach(({r, c}) => {
        gameState.grid[r][c].userVal = gameState.grid[r][c].solution;
        gameState.grid[r][c].isRevealed = true;
        gameState.grid[r][c].isRevealedByCheat = true;
        
        const el = document.getElementById(`cell-${r}-${c}`);
        if(el) {
            el.classList.remove('wrong');
            el.classList.add('revealed');
        }
    });
    // Do not auto-advance to next word
    updateUI();
    checkCompletion();
}

function revealPuzzle() {
     if(!confirm("Are you sure you want to reveal the entire puzzle?")) return;
     for(let r=0; r<puzzle.height; r++) {
        for(let c=0; c<puzzle.width; c++) {
            if (!gameState.grid[r][c].isBlack) {
                gameState.grid[r][c].userVal = gameState.grid[r][c].solution;
                gameState.grid[r][c].isRevealed = true;
                gameState.grid[r][c].isRevealedByCheat = true;
                
                const el = document.getElementById(`cell-${r}-${c}`);
                if(el) {
                    el.classList.remove('wrong');
                    el.classList.add('revealed');
                }
            }
        }
    }
    updateUI();
    checkCompletion();
}

function checkCell() {
    const { row, col } = gameState.cursor;
    if (gameState.grid[row][col].isBlack || gameState.grid[row][col].userVal === '') return;
    
    const el = document.getElementById(`cell-${row}-${col}`);
    if (gameState.grid[row][col].userVal !== gameState.grid[row][col].solution) {
        el.classList.add('wrong');
        // Remove wrong class after a delay? Or keep it? Usually keeps until changed.
        // We'll need to remove 'wrong' when user types.
    } else {
        el.classList.remove('wrong');
        // Mark as revealed (locked) if correct
        gameState.grid[row][col].isRevealed = true;
        el.classList.add('checked-correct'); // Distinct class for checked vs revealed
    }
    updateUI();
    checkCompletion();
}

function checkWord() {
    const { row, col } = gameState.cursor;
    const wordCells = getWordCells(row, col, gameState.direction);
    wordCells.forEach(({r, c}) => {
        if (gameState.grid[r][c].userVal !== '') {
            const el = document.getElementById(`cell-${r}-${c}`);
            if (gameState.grid[r][c].userVal !== gameState.grid[r][c].solution) {
                el.classList.add('wrong');
            } else {
                el.classList.remove('wrong');
                // Mark as revealed (locked) if correct
                gameState.grid[r][c].isRevealed = true;
                el.classList.add('checked-correct');
            }
        }
    });
    updateUI();
    checkCompletion();
}

function checkPuzzle() {
    for(let r=0; r<puzzle.height; r++) {
        for(let c=0; c<puzzle.width; c++) {
            if (!gameState.grid[r][c].isBlack && gameState.grid[r][c].userVal !== '') {
                 const el = document.getElementById(`cell-${r}-${c}`);
                 if (gameState.grid[r][c].userVal !== gameState.grid[r][c].solution) {
                     el.classList.add('wrong');
                 } else {
                     el.classList.remove('wrong');
                     // Mark as revealed (locked) if correct
                     gameState.grid[r][c].isRevealed = true;
                     el.classList.add('checked-correct');
                 }
            }
        }
    }
    updateUI();
    checkCompletion();
}

function renderStaticElements() {
    document.getElementById('puzzle-title').textContent = puzzle.title || 'Untitled';
    document.getElementById('puzzle-author').textContent = puzzle.author || '';
    
    const gridContainer = document.getElementById('grid-container');
    gridContainer.style.gridTemplateColumns = `repeat(${puzzle.width}, 32px)`;
    gridContainer.style.gridTemplateRows = `repeat(${puzzle.height}, 32px)`;
    
    // Adjust clues panel height dynamically based on grid + banner height roughly
    // Grid height = height * 32 + 8 (borders). Banner ~ 60. + Gap 30.
    // To match grid height exactly (last row), we should calculate just the grid's pixel height.
    // (puzzle.height * 34) + 8 + 60 + 15 = ~600.
    // If user wants it to match "the last row of the crossword", they likely mean align bottom with grid.
    // Grid container height is roughly: puzzle.height * 34 + 10 (borders).
    // We have a banner above grid (~65px with padding/margin).
    // So clues panel should be roughly Grid Height + Banner Height? 
    // Or does "match the height of the crossword grid" mean align bottoms?
    // If clues start at same top as banner (side-by-side?), no, they are side by side with grid area.
    // The structure is: Game Container -> [Puzzle Area (Banner + Grid)]  [Clues Panel]
    // So Clues Panel should equal Banner Height + Grid Height + Spacing.
    
    const bannerHeight = document.getElementById('clue-banner').offsetHeight + 13; // + margin
    // Grid height = (rows * cell_size) + (gaps * 1px) + borders (8px)
    const gridHeight = (puzzle.height * 32) + (puzzle.height - 1) + 8; 
    const totalH = bannerHeight + gridHeight;
    
    document.querySelector('.clues-panel').style.height = `${totalH}px`;
}

function renderGrid() {
    const container = document.getElementById('grid-container');
    container.innerHTML = '';
    
    for (let r = 0; r < puzzle.height; r++) {
        for (let c = 0; c < puzzle.width; c++) {
            const cellData = gameState.grid[r][c];
            const el = document.createElement('div');
            el.className = 'cell';
            el.dataset.row = r;
            el.dataset.col = c;
            el.id = `cell-${r}-${c}`;
            
            if (cellData.isBlack) {
                el.classList.add('black');
            } else {
                el.addEventListener('mousedown', (e) => handleCellClick(r, c, e));
                
                // Check for revealed state
                if (cellData.isRevealed) {
                    // Use different class based on how it was revealed (cheat vs check)
                    if (cellData.isRevealedByCheat) {
                        el.classList.add('revealed'); // Red marker
                    } else {
                        el.classList.add('checked-correct'); // Blue marker
                    }
                }

                if (cellData.number) {
                    const num = document.createElement('div');
                    num.className = 'cell-number';
                    num.textContent = cellData.number;
                    el.appendChild(num);
                }
                
                const content = document.createElement('div');
                content.className = 'cell-content';
                content.textContent = cellData.userVal;
                el.appendChild(content);
            }
            container.appendChild(el);
        }
    }
}

function renderCluesList() {
    const acrossList = document.getElementById('across-clues');
    const downList = document.getElementById('down-clues');
    
    const renderList = (cluesObj, listEl, dir) => {
        listEl.innerHTML = '';
        Object.keys(cluesObj).sort((a,b) => parseInt(a) - parseInt(b)).forEach(num => {
            const li = document.createElement('li');
            li.className = 'clue-item';
            li.dataset.number = num;
            li.dataset.dir = dir;
            li.id = `clue-${dir}-${num}`;
            li.innerHTML = `<span class="clue-num">${num}</span><span class="clue-text">${cluesObj[num]}</span>`;
            li.addEventListener('click', () => selectClue(parseInt(num), dir));
            listEl.appendChild(li);
        });
    };
    
    renderList(puzzle.acrossClues, acrossList, 'across');
    renderList(puzzle.downClues, downList, 'down');
}

function updateUI() {
    // Update grid selection
    const cells = document.querySelectorAll('.cell');
    
    // Reset classes (keep revealed/black)
    // We must NOT remove 'active' blindly if we want it to persist? 
    // No, we remove it from *all* cells, then add it back to the *current* one.
    // The issue is likely that the DOM element reference might be stale or something? No.
    // Or maybe 'active' is being removed by something else?
    
    cells.forEach(el => {
        el.classList.remove('active', 'highlight');
    });

    // Apply new classes
    const curR = gameState.cursor.row;
    const curC = gameState.cursor.col;

    // Ensure we have valid cursor before proceeding
    if (curR === undefined || curC === undefined) return;
    
    // Identify current word cells
    const wordCells = getWordCells(curR, curC, gameState.direction);
    
    wordCells.forEach(({r, c}) => {
        const el = document.getElementById(`cell-${r}-${c}`);
        if (el) {
            el.classList.add('highlight');
            // Re-add revealed class if it should be there (safety, though it shouldn't be removed)
            if (gameState.grid[r][c].isRevealed) {
                 if (gameState.grid[r][c].isRevealedByCheat) {
                     el.classList.add('revealed');
                 } else {
                     el.classList.add('checked-correct');
                 }
            }
        }
    });
    
    // Active cell
    const activeEl = document.getElementById(`cell-${curR}-${curC}`);
    if (activeEl) {
        // Force active class to be present even if revealed
        activeEl.classList.add('active');
        if (gameState.grid[curR][curC].isRevealed) {
             if (gameState.grid[curR][curC].isRevealedByCheat) {
                 activeEl.classList.add('revealed');
             } else {
                 activeEl.classList.add('checked-correct');
             }
        }
    }
    
    // Update content
    for (let r = 0; r < puzzle.height; r++) {
        for (let c = 0; c < puzzle.width; c++) {
            if (!gameState.grid[r][c].isBlack) {
                const el = document.getElementById(`cell-${r}-${c}`);
                const content = el.querySelector('.cell-content');
                const val = gameState.grid[r][c].userVal;
                content.textContent = val;
                
                // Adjust font size for Rebus
                if (val.length > 1) {
                    const len = val.length;
                    if (len <= 2) content.style.fontSize = '16px';
                    else if (len <= 3) content.style.fontSize = '12px';
                    else content.style.fontSize = '10px';
                } else {
                    content.style.fontSize = ''; // Reset to default (CSS)
                }
            }
        }
    }
    
    // Update clue banner and selection
    const currentClue = getCurrentClue();
    
    // Reset clue list selections
    document.querySelectorAll('.clue-item').forEach(item => {
        item.classList.remove('selected', 'related');
    });

    if (currentClue) {
        const dirText = gameState.direction === 'across' ? 'A' : 'D';
        // Bold number/direction, then space, then text
        document.getElementById('clue-banner').innerHTML = `<strong>${currentClue.number}${dirText}</strong>&nbsp;&nbsp;&nbsp;&nbsp;${currentClue.text}`;
        
        // Highlight primary clue
        const clueItem = document.getElementById(`clue-${gameState.direction}-${currentClue.number}`);
        if (clueItem) {
            clueItem.classList.add('selected');
            clueItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
        
        // Find and highlight related clue (the crossing clue)
        const relatedDir = gameState.direction === 'across' ? 'down' : 'across';
        // To find the number for the related clue, we need to find the start of the word in the OTHER direction at the CURRENT cursor position.
        const relatedStart = findWordStart(curR, curC, relatedDir);
        if (relatedStart) {
            const relatedCell = gameState.grid[relatedStart.r][relatedStart.c];
            if (relatedCell && relatedCell.number) {
                 const relatedItem = document.getElementById(`clue-${relatedDir}-${relatedCell.number}`);
                 if (relatedItem) {
                     relatedItem.classList.add('related');
                     relatedItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                 }
            }
        }
    }
}

function findWordStart(r, c, dir) {
    if (gameState.grid[r][c].isBlack) return null;
    let curr = dir === 'across' ? c : r;
    
    // Move back until hit black or edge
    while (curr > 0) {
        const nextR = dir === 'across' ? r : curr - 1;
        const nextC = dir === 'across' ? curr - 1 : c;
        if (gameState.grid[nextR][nextC].isBlack) break;
        curr--;
    }
    
    return dir === 'across' ? {r, c: curr} : {r: curr, c};
}

function getWordCells(r, c, dir) {
    if (gameState.grid[r][c].isBlack) return [];
    const cells = [];
    if (dir === 'across') {
        // Find start
        let start = c;
        while (start > 0 && !gameState.grid[r][start-1].isBlack) start--;
        // Find end
        let end = c;
        while (end < puzzle.width - 1 && !gameState.grid[r][end+1].isBlack) end++;
        
        for (let i = start; i <= end; i++) cells.push({r, c: i});
    } else {
        // Find start
        let start = r;
        while (start > 0 && !gameState.grid[start-1][c].isBlack) start--;
        // Find end
        let end = r;
        while (end < puzzle.height - 1 && !gameState.grid[end+1][c].isBlack) end++;
        
        for (let i = start; i <= end; i++) cells.push({r: i, c});
    }
    return cells;
}

function getCurrentClue() {
    const { row, col } = gameState.cursor;
    const start = findWordStart(row, col, gameState.direction);
    if (!start) return null;
    
    const cell = gameState.grid[start.r][start.c];
    const number = cell.number;
    
    if (!number) return null; 
    
    const text = gameState.direction === 'across' ? puzzle.acrossClues[number] : puzzle.downClues[number];
    if (!text) return { number, text: "(No clue)" };
    
    return { number, text };
}

function handleCellClick(r, c, e) {
    if (gameState.grid[r][c].isBlack) return;
    
    if (r === gameState.cursor.row && c === gameState.cursor.col) {
        gameState.direction = gameState.direction === 'across' ? 'down' : 'across';
    } else {
        gameState.cursor = { row: r, col: c };
    }
    updateUI();
}

function selectClue(number, dir) {
    gameState.direction = dir;
    // Find the cell with this number (start of word)
    let startR = -1, startC = -1;
    
    for (let r = 0; r < puzzle.height; r++) {
        for (let c = 0; c < puzzle.width; c++) {
            if (gameState.grid[r][c].number === number) {
                startR = r;
                startC = c;
                break;
            }
        }
        if (startR !== -1) break;
    }
    
    if (startR !== -1) {
        // Found the word start. Now find the first empty cell in this word.
        const wordCells = getWordCells(startR, startC, dir);
        let targetCell = wordCells[0]; // Default to start
        
        for (const cell of wordCells) {
            if (gameState.grid[cell.r][cell.c].userVal === '') {
                targetCell = cell;
                break;
            }
        }
        
        gameState.cursor = { row: targetCell.r, col: targetCell.c };
        updateUI();
    }
}

function isWordFilled(number, dir) {
    // Find start of word
    let startR, startC;
    // This is inefficient but works given we don't map number->coords directly
    for(let r=0; r<puzzle.height; r++) {
        for(let c=0; c<puzzle.width; c++) {
            if(gameState.grid[r][c].number === number) {
                startR = r; startC = c;
                break;
            }
        }
        if(startR !== undefined) break;
    }
    
    if(startR === undefined) return true; // Should not happen
    
    const cells = getWordCells(startR, startC, dir);
    return cells.every(({r, c}) => gameState.grid[r][c].userVal !== '');
}

function moveToNextLogicalClue(forward = true) {
    const currentClue = getCurrentClue();
    if (!currentClue) return;

    const currentNum = currentClue.number;
    const currentDir = gameState.direction;

    // Build full ordered list of clues: [{num, dir, isFilled}, ...]
    const allClues = [];
    
    // Across
    Object.keys(puzzle.acrossClues).sort((a,b)=>a-b).forEach(n => {
        const num = parseInt(n);
        allClues.push({ num, dir: 'across', filled: isWordFilled(num, 'across') });
    });
    // Down
    Object.keys(puzzle.downClues).sort((a,b)=>a-b).forEach(n => {
        const num = parseInt(n);
        allClues.push({ num, dir: 'down', filled: isWordFilled(num, 'down') });
    });
    
    // Find current index
    const currentIndex = allClues.findIndex(c => c.num === currentNum && c.dir === currentDir);
    if (currentIndex === -1) return;

    // Strategy:
    // 1. Look for next *unfilled* clue in sequence (wrapping around).
    // 2. If all filled, just go to next clue in sequence.
    
    let targetIndex = -1;
    
    if (forward) {
        // Check forward for unfilled
        for (let i = 1; i < allClues.length; i++) {
            const idx = (currentIndex + i) % allClues.length;
            if (!allClues[idx].filled) {
                targetIndex = idx;
                break;
            }
        }
    } else {
         // Check backward for unfilled
        for (let i = 1; i < allClues.length; i++) {
             // JS modulo on negative numbers can be tricky, add length
            const idx = (currentIndex - i + allClues.length) % allClues.length;
            if (!allClues[idx].filled) {
                targetIndex = idx;
                break;
            }
        }
    }
    
    // If found an unfilled one, go there.
    // If NOT found (targetIndex still -1), it means all are filled.
    // Then just go to immediate next/prev.
    if (targetIndex === -1) {
        if (forward) {
            targetIndex = (currentIndex + 1) % allClues.length;
        } else {
            targetIndex = (currentIndex - 1 + allClues.length) % allClues.length;
        }
    }
    
    const target = allClues[targetIndex];
    selectClue(target.num, target.dir);
}

function handleKeydown(e) {
    // Only handle if not holding modifier keys (except Shift)
    if (e.ctrlKey || e.altKey || e.metaKey) return;
    
    if (isRebusMode) return; // Ignore game keys if in rebus mode

    const { row, col } = gameState.cursor;
    
    // Prevent default scrolling for game keys
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' ', 'Backspace', 'Tab', 'Enter'].includes(e.key)) {
        e.preventDefault();
    }

    if (e.key === 'ArrowRight') {
        if (gameState.direction !== 'across') {
            gameState.direction = 'across';
            updateUI();
        } else {
            moveCursor(0, 1);
        }
    } else if (e.key === 'ArrowLeft') {
        if (gameState.direction !== 'across') {
            gameState.direction = 'across';
            updateUI();
        } else {
            moveCursor(0, -1);
        }
    } else if (e.key === 'ArrowDown') {
        if (gameState.direction !== 'down') {
            gameState.direction = 'down';
            updateUI();
        } else {
            moveCursor(1, 0);
        }
    } else if (e.key === 'ArrowUp') {
        if (gameState.direction !== 'down') {
            gameState.direction = 'down';
            updateUI();
        } else {
            moveCursor(-1, 0);
        }
    } else if (e.key === 'Backspace' || e.key === 'Delete') {
        // Behavior: 
        // 1. If current cell has content: Delete content, stay in cell.
        // 2. If current cell is empty: Move back one step (if not start), and delete that cell's content.
        
        // Prevent editing if solved
        if (gameState.isSolved) return;

        // Check if cell is revealed - if so, cannot edit
        if (gameState.grid[row][col].isRevealed) {
             // Just move back if not start
            const wordCells = getWordCells(row, col, gameState.direction);
            const isStart = wordCells.length > 0 && wordCells[0].r === row && wordCells[0].c === col;
            if (!isStart) moveCursorBack();
            updateUI();
            return;
        }

        // Remove wrong class
        const el = document.getElementById(`cell-${row}-${col}`);
        if (el) el.classList.remove('wrong');

        // Check if at start of word
        const wordCells = getWordCells(row, col, gameState.direction);
        const isStart = wordCells.length > 0 && wordCells[0].r === row && wordCells[0].c === col;
        
        if (gameState.grid[row][col].userVal !== '') {
            // Case 1: Cell has content -> Delete content, stay put
            gameState.grid[row][col].userVal = '';
        } else {
            // Case 2: Cell is empty -> Move back (if not start) and delete prev
            if (!isStart) {
                moveCursorBack();
                // After moving back, clear that cell too
                const { row: newR, col: newC } = gameState.cursor;
                // Check if new cell is revealed before clearing
                if (!gameState.grid[newR][newC].isRevealed) {
                    gameState.grid[newR][newC].userVal = '';
                    const prevEl = document.getElementById(`cell-${newR}-${newC}`);
                    if(prevEl) prevEl.classList.remove('wrong');
                }
            }
        }
        
        updateUI();
    } else if (e.key === 'Tab' || e.key === 'Enter') {
        // Explicit navigation always goes to next/prev logical clue (simple sequence)
        // Or should it also skip filled? User said "move to next clue by hitting enter or tab". 
        // Usually Tab/Enter is strict sequential navigation. 
        // But the user's latest request "Ensure that when checking which word to go to next... (a) if there are words with not-filled-in cells..."
        // implies this logic should apply generally to "next clue" actions.
        // However, explicitly skipping filled words on Tab can be annoying if you want to edit. 
        // Typically "auto-jump after typing" uses the "skip filled" logic, but Tab/Enter is "next in list".
        // BUT, the prompt says "Ensure that when checking which word to go to next... move to those first".
        // I will apply it to both for consistency based on the phrasing.
        moveToNextLogicalClue(!e.shiftKey);
    } else if (e.key.length === 1 && e.key.match(/[a-zA-Z]/)) {
        // Prevent editing if solved
        if (gameState.isSolved) return;

        // Check if cell is revealed
        if (gameState.grid[row][col].isRevealed) {
            // User wants to skip revealed cells when typing, acting as if they filled it.
            // So we essentially do the "move next" logic without changing content.
            
            // Just trigger the move logic below
        } else {
            gameState.grid[row][col].userVal = e.key.toUpperCase();
            
            // Remove wrong class if typing
            const el = document.getElementById(`cell-${row}-${col}`);
            if (el) el.classList.remove('wrong');
        }
        
        // Logic: 
        // 1. If there is a NEXT empty cell in the current word (forward search), go there.
        // 2. If NO next empty cell (we reached end or rest is filled), check if there are ANY empty cells in the word (backward search). 
        //    If yes, go to the first empty one.
        // 3. If word is completely full, move to next logical clue.
        
        const wordCells = getWordCells(row, col, gameState.direction);
        
        // Find index of current cell in the word
        let currentIndex = -1;
        for(let i=0; i<wordCells.length; i++) {
            if (wordCells[i].r === row && wordCells[i].c === col) {
                currentIndex = i;
                break;
            }
        }
        
        // 1. Search forward for next empty cell
        let targetIndex = -1;
        if (currentIndex !== -1) {
            for(let i = currentIndex + 1; i < wordCells.length; i++) {
                const c = wordCells[i];
                if (gameState.grid[c.r][c.c].userVal === '') {
                    targetIndex = i;
                    break;
                }
            }
        }
        
        // 2. If not found forward, search from start (0) up to current
        if (targetIndex === -1) {
             for(let i = 0; i < currentIndex; i++) {
                const c = wordCells[i];
                if (gameState.grid[c.r][c.c].userVal === '') {
                    targetIndex = i;
                    break;
                }
            }
        }

        if (targetIndex !== -1) {
            const target = wordCells[targetIndex];
            gameState.cursor = { row: target.r, col: target.c };
        } else {
            // 3. Word is full -> Move to next clue
            moveToNextLogicalClue(true);
        }
        
        updateUI();
        checkCompletion();
    } else if (e.key === ' ') {
        gameState.direction = gameState.direction === 'across' ? 'down' : 'across';
        updateUI();
    } 
}

function moveCursor(dr, dc) {
    let r = gameState.cursor.row + dr;
    let c = gameState.cursor.col + dc;
    
    // Simple bounds check, stop at edge
    if (r < 0 || r >= puzzle.height || c < 0 || c >= puzzle.width) return;
    
    // Stop at black squares (do not skip)
    if (gameState.grid[r][c].isBlack) return;
    
    gameState.cursor = { row: r, col: c };
    updateUI();
}

function moveCursorNext() {
    if (gameState.direction === 'across') {
        moveCursor(0, 1);
    } else {
        moveCursor(1, 0);
    }
}

function moveCursorBack() {
     if (gameState.direction === 'across') {
        moveCursor(0, -1);
    } else {
        moveCursor(-1, 0);
    }
}