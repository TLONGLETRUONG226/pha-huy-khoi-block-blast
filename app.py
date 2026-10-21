import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Block Blast Game", page_icon="🧩", layout="centered"
)

# Đọc file giao diện game html
try:
  with open("game.html", "r", encoding="utf-8") as f:
    html_content = f.read()
  components.html(html_content, height=600, scrolling=False)
except FileNotFoundError:
  st.error(
      "Chưa tìm thấy file game.html. Hãy chắc chắn bạn đã tạo file game.html"
      " trên GitHub!"
  )
