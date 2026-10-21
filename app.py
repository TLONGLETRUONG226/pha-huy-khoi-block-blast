import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Block Blast Game", page_icon="🧩", layout="centered"
)

# Mã nguồn HTML, CSS và JavaScript chuẩn cho Block Blast với nền xanh chuẩn game
html_code = """
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
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #2b82eb; /* Màu nền xanh dương chuẩn Block Blast */
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            color: white;
            overflow: hidden;
        }
        
        .header {
            margin-top: 20px;
            font-size: 32px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        /* Bảng game 8x8 */
        .board {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr);
            gap: 4px;
            width: 340px;
            height: 340px;
            background-color: #1b498c; /* Màu xanh đậm khung bảng */
            border-radius: 12px;
            padding: 8px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            margin-top: 20px;
        }
        
        .cell {
            background-color: rgba(255, 255, 255, 0.08);
            border-radius: 4px;
        }
        
        .cell.filled {
            background-color: #3182ce;
            box-shadow: inset 0 0 6px rgba(255,255,255,0.4);
        }

        /* Khung chứa 3 khối ở dưới */
        .shapes-container {
            display: flex;
            justify-content: space-around;
            align-items: center;
            width: 340px;
            height: 110px;
            margin-top: 30px;
            background-color: rgba(0, 0, 0, 0.15);
            border-radius: 12px;
            padding: 5px;
        }

        .shape-slot {
            width: 95px;
            height: 95px;
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
            width: 22px;
            height: 22px;
            border-radius: 3px;
            box-shadow: inset 0 -2px 4px rgba(0,0,0,0.3);
        }

        .block-yellow { background-color: #ecc94b; }
        .block-green { background-color: #48bb78; }
        .block-red { background-color: #f56565; }
        .block-purple { background-color: #9f7aea; }

    </style>
</head>
<body>

    <div class="header" id="score">0</div>

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

        const SHAPES = [
            { matrix: [[1]], color: 'block-yellow' },
            { matrix: [[1, 1]], color: 'block-green' },
            { matrix: [[1, 1, 1]], color: 'block-red' },
            { matrix: [[1], [1], [1]], color: 'block-purple' },
            { matrix: [[1, 1], [1, 1]], color: 'block-yellow' },
            { matrix: [[1, 0], [1, 0], [1, 1]], color: 'block-green' },
            { matrix: [[1, 1, 1], [1, 0, 0]], color: 'block-red' }
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
        }

        function renderShapeInSlot(shape, slotIndex) {
            const slot = document.getElementById(`slot-${slotIndex}`);
            slot.innerHTML = '';
            
            const shapeEl = document.createElement('div');
            shapeEl.classList.add('shape');
            shapeEl.style.gridTemplateColumns = `repeat(${shape.matrix[0].length}, 22px)`;
            
            shape.matrix.forEach(row => {
                row.forEach(val => {
                    const block = document.createElement('div');
                    if (val === 1) {
                        block.classList.add('shape-block', shape.color);
                    }
                    shapeEl.appendChild(block);
                });
            });

            enableDrag(shapeEl, slotIndex);
            slot.appendChild(shapeEl);
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
                }

                document.addEventListener('pointermove', onPointerMove);

                element.onpointerup = function(e) {
                    document.removeEventListener('pointermove', onPointerMove);
                    element.onpointerup = null;

                    element.style.display = 'none';
                    let elemBelow = document.elementFromPoint(e.clientX, e.clientY);
                    element.style.display = 'grid';

                    if (elemBelow && elemBelow.classList.contains('cell')) {
                        let r = parseInt(elemBelow.dataset.row);
                        let c = parseInt(elemBelow.dataset.col);

                        if (placeShape(currentShapes[slotIndex], r, c)) {
                            document.getElementById(`slot-${slotIndex}`).innerHTML = '';
                            currentShapes[slotIndex] = null;
                            checkAndClearLines();
                            
                            if (currentShapes.every(s => s === null)) {
                                generateShapes();
                            }
                            return;
                        }
                    }
                    element.style.position = 'static';
                };
            };
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

            rowsToClear.
