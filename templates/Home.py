import streamlit as st

st.set_page_config(page_title="หน้าแรก", layout="wide")
st.title("🏠 หน้าแรก")
st.write("ยินดีต้อนรับสู่เว็บร้านค้าออนไลน์ของเรา")

st.page_link("pages/Shop.py", label="ไปที่ร้านค้า", icon="🛒")
