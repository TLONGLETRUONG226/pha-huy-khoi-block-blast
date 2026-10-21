import base64
import streamlit as st

st.set_page_config(
    page_title="Block Blast Game", page_icon="🧩", layout="centered"
)


def get_base64_of_bin_file(bin_file):
  with open(bin_file, "rb") as f:
    data = f.read()
  return base64.b64encode(data).decode()


try:
  img_base64 = get_base64_of_bin_file("IMG_0300.jpg")
  page_bg_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
    }}
    h1, h2, h3, p, span, div {{
        color: white !important;
    }}
    </style>
    """
  st.markdown(page_bg_css, unsafe_allow_html=True)
except Exception:
  st.warning("Không thể tải ảnh nền.")

if "board" not in st.session_state:
  st.session_state.board = [[0 for _ in range(8)] for _ in range(8)]
if "score" not in st.session_state:
  st.session_state.score = 0

st.title("🧩 Block Blast")
st.write("Phiên bản Streamlit trên iPad!")
st.metric(label="Điểm số", value=st.session_state.score)

st.subheader("Bảng chơi")
for r in range(8):
  cols = st.columns(8)
  for c in range(8):
    cell_color = "🟦" if st.session_state.board[r][c] == 1 else "⬛"
    cols[c].markdown(
        f"<div style='text-align: center; font-size: 24px;'>{cell_color}</div>",
        unsafe_allow_html=True,
    )

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
  shape_type = st.radio("Chọn khối:", ["Khối đơn (1 ô)", "Khối ngang (2 ô)"])
with col2:
  r_pos = st.number_input("Hàng (0-7)", 0, 7, 0)
  c_pos = st.number_input("Cột (0-7)", 0, 7, 0)

if st.button("Đặt khối", type="primary"):
  if shape_type == "Khối đơn (1 ô)":
    if st.session_state.board[r_pos][c_pos] == 0:
      st.session_state.board[r_pos][c_pos] = 1
      st.session_state.score += 10
      st.rerun()
    else:
      st.error("Ô đã có khối!")
  elif shape_type == "Khối ngang (2 ô)":
    if (
        c_pos < 7
        and st.session_state.board[r_pos][c_pos] == 0
        and st.session_state.board[r_pos][c_pos + 1] == 0
    ):
      st.session_state.board[r_pos][c_pos] = 1
      st.session_state.board[r_pos][c_pos + 1] = 1
      st.session_state.score += 20
      st.rerun()
    else:
      st.error("Không đủ chỗ!")

if st.button("Làm mới bảng"):
  st.session_state.board = [[0 for _ in range(8)] for _ in range(8)]
  st.session_state.score = 0
  st.rerun()
