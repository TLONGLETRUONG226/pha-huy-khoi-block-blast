import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Block Blast Game", page_icon="🧩", layout="centered"
)

# Mã nguồn HTML, CSS và JavaScript hoàn chỉnh được chuyển sang mã hóa Base64 an toàn tuyệt đối
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
