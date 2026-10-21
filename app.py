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
            border
