import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Block Blast HD Premium", page_icon="🧩", layout="centered"
)

GAME_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Block Blast HD</title>
    <style>
        * { box-sizing: border-box; user-select: none; -webkit-user-select: none; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: radial-gradient(circle at center, #1e1b4b, #0f172a, #020617);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            color: #ffffff;
            overflow: hidden;
            position: relative;
            padding: 10px;
        }

        /* Ambient Glow Behind Board */
        .glow-bg {
            position: absolute;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 340px;
            height: 340px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, rgba(168, 85, 247, 0.15) 50%, rgba(0,0,0,0) 70%);
            filter: blur(30px);
            z-index: 0;
            pointer-events: none;
        }

        /* Header UI */
        .header-panel {
            position: relative;
            z-index: 10;
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 310px;
            margin-top: 5px;
            margin-bottom: 12px;
            padding: 8px 16px;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 18px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        .score-box { text-align: center; }
        .score-label { font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
        .score-val { font-size: 26px; font-weight: 950; color: #38bdf8; text-shadow: 0 0 12px rgba(56, 189, 248, 0.5); }
        .best-val { font-size: 26px; font-weight: 950; color: #facc15; text-shadow: 0 0 12px rgba(250, 204, 21, 0.5); }

        /* Praise Banner Effect */
        #praise-banner {
            position: absolute;
            top: 42%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0);
            font-size: 34px;
            font-weight: 950;
            color: #fde047;
            text-shadow: 0 4px 20px rgba(0,0,0,0.9), 0 0 15px #fde047;
            z-index: 2000;
            pointer-events: none;
            transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.35s ease;
            opacity: 0;
            white-space: nowrap;
        }
        #praise-banner.show { transform: translate(-50%, -50%) scale(1.1); opacity: 1; }

        /* Board Container */
        .board-wrapper {
            position: relative;
            z-index: 10;
            padding: 8px;
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(16px);
            border-radius: 22px;
            border: 1.5px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.1);
        }
        .board {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            grid-template-rows: repeat(7, 1fr);
            gap: 6px;
            width: 294px;
            height: 294px;
        }

        /* Cells & Blocks 3D Design */
        .cell {
            background-color: rgba(255, 255, 255, 0.04);
            border-radius: 8px;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4);
            transition: background-color 0.15s ease, border 0.15s ease;
        }
        .cell.filled {
            box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.5), 0 4px 10px rgba(0,0,0,0.4);
            border-radius: 8px;
        }

        /* Vibrant Block Color Palettes with 3D Gradients */
        .theme-cyan { background: linear-gradient(135deg, #38bdf8, #0284c7); border: 1px solid #7dd3fc; }
        .theme-yellow { background: linear-gradient(135deg, #facc15, #ca8a04); border: 1px solid #fef08a; }
        .theme-red { background: linear-gradient(135deg, #f87171, #dc2626); border: 1px solid #fca5a5; }
        .theme-green { background: linear-gradient(135deg, #4ade80, #16a34a); border: 1px solid #86efac; }
        .theme-purple { background: linear-gradient(135deg, #c084fc, #9333ea); border: 1px solid #e9d5ff; }
        .theme-orange { background: linear-gradient(135deg, #fb923c, #ea580c); border: 1px solid #fed7aa; }

        .cell.preview-valid { background-color: rgba(255, 255, 255, 0.45) !important; border: 2px dashed #ffffff; }
        .cell.preview-invalid { background-color: rgba(239, 68, 68, 0.5) !important; border: 2px dashed #ef4444; }

        .cell.clearing { animation: popExplode 0.4s cubic-bezier(0.1, 0.8, 0.3, 1) forwards; }
        @keyframes popExplode {
            0% { transform: scale(1); filter: brightness(2); }
            50% { transform: scale(1.3); background-color: #fde047; box-shadow: 0 0 25px #fde047; }
            100% { transform: scale(0); background-color: rgba(255,255,255,0.04); }
        }

        /* Shape Slots Dock */
        .shapes-dock {
            position: relative;
            z-index: 10;
            display: flex;
            justify-content: space-around;
            align-items: center;
            width: 310px;
            height: 105px;
            margin-top: 14px;
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(14px);
            border-radius: 20px;
            padding: 8px;
            border: 1.5px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 12px 30px rgba(0,0,0,0.5);
        }
        .shape-slot {
            width: 90px;
            height: 90px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .shape {
            display: grid;
            gap: 3px;
            cursor: grab;
            touch-action: none;
            filter: drop-shadow(0 6px 12px rgba(0,0,0,0.5));
            transition: transform 0.1s ease;
        }
        .shape:active { cursor: grabbing; transform: scale(1.1); }
        .shape-block {
            width: 17px;
            height: 17px;
            border-radius: 5px;
            box-shadow: inset 0 1.5px 3px rgba(255,255,255,0.6), inset 0 -2px 4px rgba(0,0,0,0.4);
        }

        /* Start Menu Modal */
        #start-menu {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(10, 15, 30, 0.95);
            backdrop-filter: blur(16px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 4000;
            padding: 20px;
        }
        #start-menu h1 {
            font-size: 44px;
            color: #facc15;
            margin-bottom: 30px;
            text-shadow: 0 0 25px rgba(250, 204, 21, 0.7), 0 4px 12px rgba(0,0,0,0.9);
            text-align: center;
            font-weight: 950;
            letter-spacing: 2px;
        }
        .btn-primary {
            padding: 16px 44px;
            background: linear-gradient(135deg, #22c55e, #15803d);
            color: white;
            border: none;
            border-radius: 20px;
            font-size: 22px;
            font-weight: 900;
            cursor: pointer;
            box-shadow: 0 10px 30px rgba(34, 197, 94, 0.5);
            transition: all 0.2s ease;
            border: 2px solid rgba(255,255,255,0.25);
        }
        .btn-primary:active { transform: scale(0.95); }

        /* Game Over Modal */
        #game-over-modal {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(16px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 3000;
            display: none;
            padding: 20px;
            text-align: center;
        }
        #game-over-modal h1 {
            font-size: 44px;
            color: #ef4444;
            margin-bottom: 8px;
            text-shadow: 0 0 30px rgba(239, 68, 68, 0.8);
            font-weight: 950;
        }
        .taunt-msg {
            font-size: 22px;
            color: #facc15;
            margin-bottom: 20px;
            font-weight: 800;
            text-shadow: 0 2px 10px rgba(0,0,0,0.8);
            line-height: 1.4;
        }
        #game-over-modal p {
            font-size: 18px;
            margin-bottom: 25px;
            color: #cbd5e1;
            font-weight: 600;
        }
        .btn-restart {
            padding: 14px 36px;
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            border: none;
            border-radius: 18px;
            font-size: 20px;
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5);
            border: 2px solid rgba(255,255,255,0.2);
        }
        .btn-restart:active { transform: scale(0.95); }
    </style>
</head>
<body>
    <div class="glow-bg"></div>

    <div id="start-menu">
        <h1>🧩 BLOCK BLAST</h1>
        <button class="btn-primary" onclick="launchGame()">▶ BẮT ĐẦU CHƠI</button>
    </div>

    <div class="header-panel">
        <div class="score-box">
            <div class="score-label">Điểm số</div>
            <div class="score-val" id="score">0</div>
        </div>
        <div class="score-box">
            <div class="score-label">Kỷ lục</div>
            <div class="best-val" id="best-score">0</div>
        </div>
    </div>

    <div id="praise-banner">Tuyệt vời!</div>

    <div id="game-over-modal">
        <h1>GAME OVER!</h1>
        <div class="taunt-msg">chơi gà quá, chơi lạii đi hahaa 🤪</div>
        <p>Tổng điểm của bạn: <span id="final-score" style="color:#38bdf8; font-weight:800;">0</span></p>
        <button class="btn-restart" onclick="restartGame()">Thử Lại Ngay</button>
    </div>

    <div class="board-wrapper">
        <div class="board" id="board"></div>
    </div>

    <div class="shapes-dock" id="shapes-dock">
        <div class="shape-slot" id="slot-0"></div>
        <div class="shape-slot" id="slot-1"></div>
        <div class="shape-slot" id="slot-2"></div>
    </div>

    <script>
        const BOARD_SIZE = 7;
        let boardState = Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(0));
        let score = 0;
        let bestScore = localStorage.getItem('block_blast_best') || 0;
        let audioCtx = null;

        document.getElementById('best-score').innerText = bestScore;

        const praises = ["🌟 Quá đỉnh!", "🔥 Tuyệt vời!", "🚀 Xuất sắc!", "💎 Siêu sao!", "🎉 Combo đỉnh cao!"];

        // Unlock audio context silently without playing laugh
        function launchGame() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            document.getElementById('start-menu').style.display = 'none';
        }

        // Web Audio Synthesizer
        function playSound(type) {
            if (!audioCtx) return;
            let now = audioCtx.currentTime;

            if (type === 'place') {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.type = 'sine';
                osc.frequency.setValueAtTime(360, now);
                osc.frequency.exponentialRampToValueAtTime(180, now + 0.09);
                gain.gain.setValueAtTime(0.35, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.09);
                osc.start(now);
                osc.stop(now + 0.09);
            } 
            else if (type === 'clear') {
                [500, 700, 950, 1300].forEach((freq, idx) => {
                    let o = audioCtx.createOscillator();
                    let g = audioCtx.createGain();
                    o.connect(g);
                    g.connect(audioCtx.destination);
                    o.type = 'triangle';
                    o.frequency.setValueAtTime(freq, now + idx * 0.06);
                    g.gain.setValueAtTime(0.3, now + idx * 0.06);
                    g.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.06 + 0.14);
                    o.start(now + idx * 0.06);
                    o.stop(now + idx * 0.06 + 0.14);
                });
            } 
            else if (type === 'gameover') {
                // Tiếng cười khà khà lém lỉnh, khiêu khích CHỈ PHÁT KHI THUA GAME
                const laughNotes = [
                    { t: 0.00, f: 520, d: 0.12 },
                    { t: 0.13, f: 650, d: 0.12 },
                    { t: 0.26, f: 520, d: 0.12 },
                    { t: 0.39, f: 680, d: 0.14 },
                    { t: 0.55, f: 550, d: 0.12 },
                    { t: 0.70, f: 720, d: 0.16 },
                    { t: 0.88, f: 400, d: 0.28 }
                ];
                laughNotes.forEach(note => {
                    let o = audioCtx.createOscillator();
                    let g = audioCtx.createGain();
                    o.connect(g);
                    g.connect(audioCtx.destination);
                    o.type = 'sawtooth';
                    o.frequency.setValueAtTime(note.f, now + note.t);
                    g.gain.setValueAtTime(0.45, now + note.t);
                    g.gain.exponentialRampToValueAtTime(0.001, now + note.t + note.d);
                    o.start(now + note.t);
                    o.stop(now + note.t + note.d);
                });
            }
        }

        function showPraise() {
            const banner = document.getElementById('praise-banner');
            banner.innerText = praises[Math.floor(Math.random() * praises.length)];
            banner.classList.add('show');
            setTimeout(() => banner.classList.remove('show'), 900);
        }

        const SHAPES = [
            { matrix: [[1]], theme: 'theme-yellow' },
            { matrix: [[1, 1]], theme: 'theme-green' },
            { matrix: [[1], [1]], theme: 'theme-green' },
            { matrix: [[1, 1, 1]], theme: 'theme-red' },
            { matrix: [[1], [1], [1]], theme: 'theme-red' },
            { matrix: [[1, 1, 1, 1]], theme: 'theme-cyan' },
            { matrix: [[1], [1], [1], [1]], theme: 'theme-cyan' },
            { matrix: [[1, 1], [1, 1]], theme: 'theme-yellow' },
            { matrix: [[1, 1, 1], [1, 1, 1], [1, 1, 1]], theme: 'theme-orange' },
            { matrix: [[1, 0], [1, 0], [1, 1]], theme: 'theme-purple' },
            { matrix: [[0, 1], [0, 1], [1, 1]], theme: 'theme-purple' },
            { matrix: [[1, 1, 1], [1, 0, 0]], theme: 'theme-orange' },
            { matrix: [[1, 1, 1], [0, 0, 1]], theme: 'theme-orange' },
            { matrix: [[1, 1, 1], [0, 1, 0]], theme: 'theme-green' },
            { matrix: [[0, 1, 0], [1, 1, 1]], theme: 'theme-green' },
            { matrix: [[1, 0], [1, 1], [1, 0]], theme: 'theme-green' },
            { matrix: [[1, 1, 0], [0, 1, 1]], theme: 'theme-red' },
            { matrix: [[0, 1, 1], [1, 1, 0]], theme: 'theme-red' }
        ];

        let currentShapes = [null, null, null];
        const boardEl = document.getElementById('board');

        for (let r = 0; r < BOARD_SIZE; r++) {
            for (let c = 0; c < BOARD_SIZE; c++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.dataset.row = r;
                cell.dataset.col = c;
                boardEl.appendChild(cell);
            }
        }

        function generateShapes() {
            for (let i = 0; i < 3; i++) {
                if (!currentShapes[i]) {
                    const randomShape = SHAPES[Math.floor(Math.random() * SHAPES.length)];
                    currentShapes[i] = randomShape;
                    renderShapeInSlot(randomShape, i);
                }
            }
            checkGameOver();
        }

        function renderShapeInSlot(shape, slotIndex) {
            const slot = document.getElementById('slot-' + slotIndex);
            slot.innerHTML = '';
            const shapeEl = document.createElement('div');
            shapeEl.classList.add('shape');
            shapeEl.style.gridTemplateColumns = `repeat(${shape.matrix[0].length}, 17px)`;

            shape.matrix.forEach(row => {
                row.forEach(val => {
                    const block = document.createElement('div');
                    if (val === 1) {
                        block.classList.add('shape-block', shape.theme);
                    } else {
                        block.style.width = '17px';
                        block.style.height = '17px';
                    }
                    shapeEl.appendChild(block);
                });
            });

            enableDrag(shapeEl, slotIndex);
            slot.appendChild(shapeEl);
        }

        function clearPreviews() {
            document.querySelectorAll('.cell').forEach(c => {
                c.classList.remove('preview-valid', 'preview-invalid');
            });
        }

        function enableDrag(element, slotIndex) {
            element.onpointerdown = function(e) {
                e.preventDefault();
                element.style.position = 'fixed';
                element.style.zIndex = 1000;
                moveAt(e.clientX, e.clientY);

                function moveAt(pageX, pageY) {
                    element.style.left = pageX - element.offsetWidth / 2 + 'px';
                    element.style.top = pageY - element.offsetHeight / 2 + 'px';
                }

                function onPointerMove(e) {
                    moveAt(e.clientX, e.clientY);
                    element.style.display = 'none';
                    let elemBelow = document.elementFromPoint(e.clientX, e.clientY);
                    element.style.display = 'grid';
                    clearPreviews();
                    if (elemBelow && elemBelow.classList.contains('cell')) {
                        let r = parseInt(elemBelow.dataset.row);
                        let c = parseInt(elemBelow.dataset.col);
                        showPreview(currentShapes[slotIndex], r, c);
                    }
                }

                document.addEventListener('pointermove', onPointerMove);

                element.onpointerup = function(e) {
                    document.removeEventListener('pointermove', onPointerMove);
                    element.onpointerup = null;
                    clearPreviews();
                    element.style.display = 'none';
                    let elemBelow = document.elementFromPoint(e.clientX, e.clientY);
                    element.style.display = 'grid';

                    if (elemBelow && elemBelow.classList.contains('cell')) {
                        let r = parseInt(elemBelow.dataset.row);
                        let c = parseInt(elemBelow.dataset.col);
                        if (placeShape(currentShapes[slotIndex], r, c)) {
                            playSound('place');
                            document.getElementById('slot-' + slotIndex).innerHTML = '';
                            currentShapes[slotIndex] = null;
                            checkAndClearLines();
                            if (currentShapes.every(s => s === null)) {
                                generateShapes();
                            } else {
                                checkGameOver();
                            }
                            return;
                        }
                    }
                    element.style.position = 'static';
                };
            };
        }

        function showPreview(shape, r, c) {
            let canPlace = true;
            for (let row = 0; row < shape.matrix.length; row++) {
                for (let col = 0; col < shape.matrix[row].length; col++) {
                    if (shape.matrix[row][col] === 1) {
                        let targetR = r + row;
                        let targetC = c + col;
                        if (targetR >= BOARD_SIZE || targetC >= BOARD_SIZE || boardState[targetR][targetC] !== 0) {
                            canPlace = false;
                        }
                    }
                }
            }
            for (let row = 0; row < shape.matrix.length; row++) {
                for (let col = 0; col < shape.matrix[row].length; col++) {
                    if (shape.matrix[row][col] === 1) {
                        let targetR = r + row;
                        let targetC = c + col;
                        if (targetR < BOARD_SIZE && targetC < BOARD_SIZE) {
                            let cell = boardEl.children[targetR * BOARD_SIZE + targetC];
                            cell.classList.add(canPlace ? 'preview-valid' : 'preview-invalid');
                        }
                    }
                }
            }
        }

        function placeShape(shape, r, c) {
            for (let row = 0; row < shape.matrix.length; row++) {
                for (let col = 0; col < shape.matrix[row].length; col++) {
                    if (shape.matrix[row][col] === 1) {
                        let targetR = r + row;
                        let targetC = c + col;
                        if (targetR >= BOARD_SIZE || targetC >= BOARD_SIZE || boardState[targetR][targetC] !== 0) {
                            return false;
                        }
                    }
                }
            }
            for (let row = 0; row < shape.matrix.length; row++) {
                for (let col = 0; col < shape.matrix[row].length; col++) {
                    if (shape.matrix[row][col] === 1) {
                        boardState[r + row][c + col] = shape.theme;
                        let cell = boardEl.children[(r + row) * BOARD_SIZE + (c + col)];
                        cell.classList.add('filled', shape.theme);
                    }
                }
            }
            score += 10;
            updateScores();
            return true;
        }

        function checkAndClearLines() {
            let rowsToClear = [];
            let colsToClear = [];

            for (let r = 0; r < BOARD_SIZE; r++) {
                if (boardState[r].every(val => val !== 0)) rowsToClear.push(r);
            }
            for (let c = 0; c < BOARD_SIZE; c++) {
                let full = true;
                for (let r = 0; r < BOARD_SIZE; r++) {
                    if (boardState[r][c] === 0) full = false;
                }
                if (full) colsToClear.push(c);
            }

            if (rowsToClear.length > 0 || colsToClear.length > 0) {
                playSound('clear');
                showPraise();
            }

            rowsToClear.forEach(r => {
                for (let c = 0; c < BOARD_SIZE; c++) {
                    let oldTheme = boardState[r][c];
                    boardState[r][c] = 0;
                    let cell = boardEl.children[r * BOARD_SIZE + c];
                    cell.classList.add('clearing');
                    setTimeout(() => cell.classList.remove('filled', 'clearing', oldTheme), 400);
                }
                score += 100;
            });

            colsToClear.forEach(c => {
                for (let r = 0; r < BOARD_SIZE; r++) {
                    let oldTheme = boardState[r][c];
                    boardState[r][c] = 0;
                    let cell = boardEl.children[r * BOARD_SIZE + c];
                    cell.classList.add('clearing');
                    setTimeout(() => cell.classList.remove('filled', 'clearing', oldTheme), 400);
                }
                score += 100;
            });

            updateScores();
        }

        function updateScores() {
            document.getElementById('score').innerText = score;
            if (score > bestScore) {
                bestScore = score;
                localStorage.setItem('block_blast_best', bestScore);
                document.getElementById('best-score').innerText = bestScore;
            }
        }

        function checkGameOver() {
            let canMove = false;
            for (let i = 0; i < 3; i++) {
                let shape = currentShapes[i];
                if (!shape) continue;

                for (let r = 0; r < BOARD_SIZE; r++) {
                    for (let c = 0; c < BOARD_SIZE; c++) {
                        let valid = true;
                        for (let row = 0; row < shape.matrix.length; row++) {
                            for (let col = 0; col < shape.matrix[row].length; col++) {
                                if (shape.matrix[row][col] === 1) {
                                    let targetR = r + row;
                                    let targetC = c + col;
                                    if (targetR >= BOARD_SIZE || targetC >= BOARD_SIZE || boardState[targetR][targetC] !== 0) {
                                        valid = false;
                                        break;
                                    }
                                }
                            }
                            if (!valid) break;
                        }
                        if (valid) { canMove = true; break; }
                    }
                    if (canMove) break;
                }
                if (canMove) break;
            }

            if (!canMove && currentShapes.some(s => s !== null)) {
                playSound('gameover');
                document.getElementById('final-score').innerText = score;
                document.getElementById('game-over-modal').style.display = 'flex';
            }
        }

        function restartGame() {
            boardState = Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(0));
            score = 0;
            updateScores();

            document.querySelectorAll('.cell').forEach(c => {
                c.className = 'cell';
            });

            currentShapes = [null, null, null];
            document.getElementById('game-over-modal').style.display = 'none';
            generateShapes();
        }

        generateShapes();
    </script>
</body>
</html>
"""

components.html(GAME_HTML, height=620, scrolling=False)
