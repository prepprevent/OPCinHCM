import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen

st.set_page_config(layout="wide")

# Đọc file Excel
file_path = "dieu tri.xlsx"
df = pd.read_excel(file_path)

# Chuẩn hóa cột Số BN về dạng số
df["Số BN"] = pd.to_numeric(df["Số BN"], errors="coerce")

st.title("Bản đồ cơ sở điều trị tại TP Hồ Chí Minh")

# Hàm phân màu theo số bệnh nhân
def get_color(so_bn):
    if pd.isna(so_bn):
        return "gray"
    elif so_bn < 100:
        return "#fee5d9"
    elif so_bn < 500:
        return "#fcae91"
    elif so_bn < 1000:
        return "#fb6a4a"
    else:
        return "#cb181d"

# Tạo bản đồ
m = folium.Map(
    location=[df["lat"].mean(), df["lon"].mean()],
    zoom_start=10
)
Fullscreen(position="topright").add_to(m)

# Vẽ các điểm
for _, row in df.iterrows():
    color = get_color(row["Số BN"])

    tooltip_text = f"{row['Tên cơ sở']}<br>Số BN: {int(row['Số BN']) if pd.notna(row['Số BN']) else 'Không có dữ liệu'}"

    popup_text = f"""
    <b>{row['Tên cơ sở']}</b><br>
    STT: {row['STT']}<br>
    Địa chỉ: {row['Địa chỉ']}<br>
    Điện thoại: {row['Điện thoại liên hệ']}<br>
    Số BN: {int(row['Số BN']) if pd.notna(row['Số BN']) else 'Không có dữ liệu'}
    """

    folium.Marker(
        location=[row["lat"], row["lon"]],
        tooltip=folium.Tooltip(tooltip_text),
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color=color)
    ).add_to(m)

# Hiển thị bản đồ
st_folium(m, use_container_width=True, height=800)

# Chú giải màu
st.subheader("Chú giải màu theo số bệnh nhân")
legend_df = pd.DataFrame({
    "Nhóm số BN": ["< 100", "100 - < 500", "500 - < 1000", ">= 1000"],
    "Màu": ["green", "blue", "orange", "red"]
})
st.dataframe(legend_df, use_container_width=True)
