import streamlit as st
import pymysql
import os
from dotenv import load_dotenv
from pathlib import Path

# โหลดค่าจาก .env
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

def load_products():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
                SELECT p.id, p.category, p.name_th, p.name_en, p.stock, p.price, pi.image_path
                FROM products p
                LEFT JOIN product_images pi ON p.id = pi.product_id
                GROUP BY p.id
            """
            cursor.execute(sql)
            return cursor.fetchall()

st.set_page_config(page_title="ร้านค้า", layout="wide")
st.title("🛒 ร้านค้า")

products = load_products()

if not products:
    st.info("ไม่มีสินค้าในฐานข้อมูล")
else:
    cols = st.columns(4)

    for i, product in enumerate(products):
        col = cols[i % 4]
        with col:
            st.markdown(f"### {product['name_th']} / {product['name_en']}")
            st.write(f"หมวดหมู่: {product['category']}")
            st.write(f"ราคา: {product['price']:,} บาท")
            st.write(f"จำนวนในสต็อก: {product['stock']} ชิ้น")

            image_path = product.get("image_path")
            if image_path and Path(image_path).exists():
                st.image(image_path, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/150?text=No+Image", use_container_width=True)

            if st.button(f"ซื้อ {product['name_th']}", key=f"buy_{product['id']}"):
                st.success(f"เพิ่ม {product['name_th']} ลงตะกร้าแล้ว!")
