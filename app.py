import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Block Blast Game", page_icon="🧩", layout="centered"
)

# Chuyển ảnh IMG_0300.jpg sang dạng Base64 trực tiếp nếu có, hoặc tạo giao diện chơi kéo thả chuẩn
image_base64_str = ""
try:
  with open("IMG_0300.jpg", "rb") as image_file:
    image_base64_str = base64.b64encode(image_file.read()).decode("utf-8")
except Exception:
  image_base64_str = ""

# Mã nguồn HTML, CSS và JavaScript tạo game Block Blast kéo thả
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
        }}
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #1a1a2e;
            background-image: {'url("data:image/jpeg;base64,' + image_base64_str + '")' if image_base64_str else 'none'};
            background-size: cover;
            background-position: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            color: white;
        }}
        
        .header {{
            margin-top: 20px;
            font-size: 28px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }}
        
        /* Bảng game 8x8 */
        .board {{
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr);
            gap: 4px;
            width: 340px;
            height: 340px;
            background-color: rgba(10, 25, 47, 0.85);
            border-radius: 12px;
            padding: 8px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.5);
            margin-top: 15px;
        }}
        
        .cell {{
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            transition: background-color 0.2s;
        }}
        
        .cell.filled {{
            background-color: #3182ce;
            box-shadow: inset 0 0 5px rgba(255,255,255,0.5);
        }}
        
        .cell.hover {{
            background-color: rgba(255, 255, 255, 0.4);
        }}

        /* Thùng chứa 3 khối ở dưới */
        .shapes-container {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            width: 360px;
            height: 120px;
            margin-top: 30px;
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            padding: 10px;
        }}

        .shape-slot {{
            width: 90px;
            height: 90px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .shape {{
            display: grid;
            gap: 2px;
            cursor: grab;
            touch-action: none;
        }}

        .shape-block {{
            width: 22px;
            height:
