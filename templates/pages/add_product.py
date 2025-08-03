import streamlit as st
import pymysql
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

def save_image(uploaded_file):
    save_dir = Path("product_images")
    save_dir.mkdir(exist_ok=True)
    save_path = save_dir / uploaded_file.name
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(save_path)

def insert_product(category, name_th, name_en, stock, price, image_path=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # เพิ่มข้อมูลสินค้า
            sql = """
                INSERT INTO products (category, name_th, name_en, stock, price)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (category, name_th, name_en, stock, price))
            product_id = cursor.lastrowid  # ได้ id สินค้าใหม่

            # ถ้ามีภาพให้เพิ่มใน product_images
            if image_path:
                sql_img = """
                    INSERT INTO product_images (product_id, image_path)
                    VALUES (%s, %s)
                """
                cursor.execute(sql_img, (product_id, image_path))

        conn.commit()

# ===========================
# UI หน้าเพิ่มสินค้า
# ===========================
st.set_page_config(page_title="เพิ่มสินค้า", layout="wide")
st.title("➕ เพิ่มสินค้าใหม่")

with st.form("add_product_form"):
    category = st.text_input("หมวดหมู่สินค้า", max_chars=100)
    name_th = st.text_input("ชื่อสินค้า (ไทย)", max_chars=255)
    name_en = st.text_input("ชื่อสินค้า (อังกฤษ)", max_chars=255)
    stock = st.number_input("จำนวนในสต็อก", min_value=0, step=1)
    price = st.number_input("ราคา (บาท)", min_value=0.0, format="%.2f")
    uploaded_file = st.file_uploader("อัปโหลดภาพสินค้า (ไฟล์ .jpg, .png)", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("เพิ่มสินค้า")

    if submitted:
        if not (category and name_th and name_en):
            st.error("กรุณากรอกหมวดหมู่ และชื่อสินค้าทั้งภาษาไทยและอังกฤษ")
        else:
            image_path = None
            if uploaded_file is not None:
                image_path = save_image(uploaded_file)

            try:
                insert_product(category, name_th, name_en, stock, price, image_path)
                st.success(f"เพิ่มสินค้า '{name_th}' เรียบร้อยแล้ว")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
