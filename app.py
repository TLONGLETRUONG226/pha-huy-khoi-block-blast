import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Block Blast Game", page_icon="🧩", layout="centered"
)

GAME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
        }
        body {
            margin: 0;
            padding: 5px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #2b82eb;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            color: white;
            overflow: hidden;
            position: relative;
        }
        .header {
            margin-top: 5px;
            font-size: 24px;
            font-weight: 800;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        }
        .start-btn {
            margin: 4px 0;
            padding: 6px 14px;
            background-color: #f59e0b;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            z-index: 100;
        }
        
        #praise-banner {
            position: absolute;
            top: 38%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0);
            font-size: 28px;
            font-weight: 900;
            color: #ffeb3b;
            text-shadow: 3px 3px 8px rgba(0,0,0,0.8);
            z-index: 2000;
            pointer-events: none;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s ease;
            opacity: 0;
            white-space: nowrap;
        }
        #praise-banner.show {
            transform: translate(-50%, -50%) scale(1);
            opacity: 1;
        }

        /* Màn hình Game Over */
        #game-over-modal {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.85);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 3000;
            display: none;
        }
        #game-over-modal h1 {
            font-size: 36px;
            color: #ef4444;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
        }
        #game-over-modal p {
            font-size: 20px;
            margin-bottom: 20px;
        }
        .restart-btn {
            padding: 10px 24px;
            background-color: #22c55e;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }

        /* Bảng chơi được thu gọn */
        .board {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr);
            gap: 3px;
            width: 290px;
            height: 290px;
            background-color: #1b498c;
            border-radius: 10px;
            padding: 6px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.4);
            margin-top: 5px;
            position: relative;
        }
        .cell {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
        }
        .cell.filled {
            background-color: #3182ce;
            box-shadow: inset 0 0 6px rgba(255,255,255,0.5);
        }
        .cell.preview-valid {
            background-color: rgba(255, 255, 255, 0.5) !important;
            border: 2px dashed #ffffff;
        }
        .cell.preview-invalid {
            background-color: rgba(239, 68, 68, 0.5) !important;
        }

        .cell.clearing {
            animation: explodeCell 0.4s ease-out forwards;
        }
        @keyframes explodeCell {
            0% { transform: scale(1); background-color: #ffeb3b; box-shadow: 0 0 10px #ffeb3b; }
            50% { transform: scale(1.3); background-color: #ef4444; }
            100% { transform: scale(0); background-color: rgba(255,255,255,0.1); }
        }

        /* Khung chứa 3 khối gọn gàng */
        .shapes-container {
            display: flex;
            justify-content: space-around;
            align-items: center;
            width: 290px;
            height: 90px;
            margin-top: 10px;
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 4px;
        }
        .shape-slot {
            width: 85px;
            height: 80px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .shape {
            display: grid;
            gap: 2px;
            cursor: grab;
            touch-action: none;
        }
        .shape-block {
            width: 15px;
            height: 15px;
            border-radius: 3px;
            box-shadow: inset 0 -2px 4px rgba(0,0,0,0.3);
        }
        .block-yellow { background-color: #ecc94b; }
        .block-green { background-color: #48bb78; }
        .block-red { background-color: #f56565; }
        .block-purple { background-color: #9f7aea; }
        .block-cyan { background-color: #38bdf8; }
        .block-orange { background-color: #fb923c; }

    </style>
</head>
<body>

    <div class="header">Điểm: <span id="score">0</span></div>
    <button class="start-btn" id="startBtn" onclick="startGame()">▶ Bật âm thanh & Chơi ngay</button>

    <div id="praise-banner">Tuyệt vời!</div>

    <div id="game-over-modal">
        <h1>GAME OVER!</h1>
        <p>Tổng điểm của bạn: <span id="final-score">0</span></p>
        <button class="restart-btn" onclick="restartGame()">Chơi Lại</button>
    </div>

    <div class="board" id="board"></div>

    <div class="shapes-container" id="shapes-container">
        <div class="shape-slot" id="slot-0"></div>
        <div class="shape-slot" id="slot-1"></div>
        <div class="shape-slot" id="slot-2"></div>
    </div>

    <script>
        const BOARD_SIZE = 8;
        let boardState = Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(0));
        let score = 0;
        let audioCtx = null;

        const praises = ["🌟 Quá đỉnh!", "🔥 Tuyệt vời!", "🚀 Xuất sắc!", "💎 Siêu sao!", "🎉 Combo đỉnh cao!"];

        function startGame() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            document.getElementById('startBtn').style.display = 'none';
        }

        function playSound(type) {
            if (!audioCtx) return;
            if (type === 'place') {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.type = 'sine';
                osc.frequency.setValueAtTime(300, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(150, audioCtx.currentTime + 0.1);
                gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.1);
            } else if (type === 'clear') {
                let now = audioCtx.currentTime;
                [400, 600, 800, 1050].forEach((freq, index) => {
                    let o = audioCtx.createOscillator();
                    let g = audioCtx.createGain();
                    o.connect(g);
                    g.connect(audioCtx.destination);
                    o.type = 'triangle';
                    o.frequency.setValueAtTime(freq, now + index * 0.08);
                    g.gain.setValueAtTime(0.3, now + index * 0.08);
                    g.gain.exponentialRampToValueAtTime(0.01, now + index * 0.08 + 0.15);
                    o.start(now + index * 0.08);
                    o.stop(now + index * 0.08 + 0.15);
                });
            } else if (type === 'gameover') {
                let now = audioCtx.currentTime;
                [300, 250, 200, 150].forEach((freq, index) => {
                    let o = audioCtx.createOscillator();
                    let g = audioCtx.createGain();
                    o.connect(g);
                    g.connect(audioCtx.destination);
                    o.type = 'sawtooth';
                    o.frequency.setValueAtTime(freq, now + index * 0.12);
                    g.gain.setValueAtTime(0.3, now + index * 0.12);
                    g.gain.exponentialRampToValueAtTime(0.01, now + index * 0.12 + 0.2);
                    o.start(now + index * 0.12);
                    o.stop(now + index * 0.12 + 0.2);
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
            { matrix: [[1]], color: 'block-yellow' },
            { matrix: [[1, 1]], color: 'block-green' },
            { matrix: [[1], [1]], color: 'block-green' },
            { matrix: [[1, 1, 1]], color: 'block-red' },
            { matrix: [[1], [1], [1]], color: 'block-red' },
            { matrix: [[1, 1, 1, 1]], color: 'block-cyan' },
            { matrix: [[1], [1], [1], [1]], color: 'block-cyan' },
            { matrix: [[1, 1], [1, 1]], color: 'block-yellow' },
            { matrix: [[1, 1, 1], [1, 1, 1], [1, 1, 1]], color: 'block-orange' },
            { matrix: [[1, 0], [1, 0], [1, 1]], color: 'block-purple' },
            { matrix: [[0, 1], [0, 1], [1, 1]], color: 'block-purple' },
            { matrix: [[1, 1, 1], [1, 0, 0]], color: 'block-orange' },
            { matrix: [[1, 1, 1], [0, 0, 1]], color: 'block-orange' },
            { matrix: [[1, 1, 1], [0, 1, 0]], color: 'block-green' },
            { matrix: [[0, 1, 0], [1, 1, 1]], color: 'block-green' },
            { matrix: [[1, 0], [1, 1], [1, 0]], color: 'block-green' },
            { matrix: [[1, 1, 0], [0, 1, 1]], color: 'block-red' },
            { matrix: [[0, 1, 1], [1, 1, 0]], color: 'block-red' }
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
            const slot = document.getElementById("slot-" + slotIndex);
            slot.innerHTML = '';
            
            const shapeEl = document.createElement('div');
            shapeEl.classList.add('shape');
            shapeEl.style.gridTemplateColumns = `repeat(${shape.matrix[0].length}, 15px)`;
            
            shape.matrix.forEach(row => {
                row.forEach(val => {
                    const block = document.createElement('div');
                    if (val === 1) {
                        block.classList.add('shape-block', shape.color);
                    } else {
                        block.style.width = '15px';
                        block.style.height = '15px';
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
                            document.getElementById("slot-" + slotIndex).innerHTML = '';
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
                        if (targetR >= BOARD_SIZE || targetC >= BOARD_SIZE || boardState[targetR][targetC] === 1) {
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
                        if (targetR >= BOARD_SIZE || targetC >= BOARD_SIZE || boardState[targetR][targetC] === 1) {
                            return false;
                        }
                    }
                }
            }

            for (let row = 0; row < shape.matrix.length; row++) {
                for (let col = 0; col < shape.matrix[row].length; col++) {
                    if (shape.matrix[row][col] === 1) {
                        boardState[r + row][c + col] = 1;
                        let cell = boardEl.children[(r + row) * BOARD_SIZE + (c + col)];
                        cell.classList.add('filled');
                    }
                }
            }
            score += 10;
            document.getElementById('score').innerText = score;
            return true;
        }

        function checkAndClearLines() {
            let rowsToClear = [];
            let colsToClear = [];

            for (let r = 0; r < BOARD_SIZE; r++) {
                if (boardState[r].every(val => val === 1)) {
                    rowsToClear.push(r);
                }
            }

            for (let c = 0; c < BOARD_SIZE; c++) {
                let full = true;
                for (let r = 0; r < BOARD_SIZE; r++) {
                    if (boardState[r][c] !== 1) full = false;
                }
                if (full) colsToClear.push(c);
            }

            if (rowsToClear.length > 0 || colsToClear.length > 0) {
                playSound('clear');
                showPraise();
            }

            rowsToClear.forEach(r => {
                for (let c = 0; c < BOARD_SIZE; c++) {
                    boardState[r][c] = 0;
                    let cell = boardEl.children[r * BOARD_SIZE + c];
                    cell.classList.add('clearing');
                    setTimeout(() => cell.classList.remove('filled', 'clearing'), 400);
                }
                score += 100;
            });

            colsToClear.forEach(c => {
                for (let r = 0; r < BOARD_SIZE; r++) {
                    boardState[r][c] = 0;
                    let cell = boardEl.children[r * BOARD_SIZE + c];
                    cell.classList.add('clearing');
                    setTimeout(() => cell.classList.remove('filled', 'clearing'), 400);
                }
                score += 100;
            });

            document.getElementById('score').innerText = score;
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
                                    if (targetR >= BOARD_SIZE || targetC >= BOARD_SIZE || boardState[targetR][targetC] === 1) {
                                        valid = false;
                                        break;
                                    }
                                }
                            }
                            if (!valid) break;
                        }
                        if (valid) {
                            canMove = true;
                            break;
                        }
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
            document.getElementById('score').innerText = score;
            document.querySelectorAll('.cell').forEach(c => c.classList.remove('filled', 'clearing'));
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
