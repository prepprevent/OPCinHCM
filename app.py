import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen

st.set_page_config(layout="wide")

# Đọc file Excel
file_path = "dieu tri.xlsx"
df = pd.read_excel(file_path)

# Bỏ các dòng thiếu tọa độ
df = df.dropna(subset=["lat", "lon"])

st.title("Bản đồ cơ sở điều trị")

# Tạo bảng màu theo STT
unique_stt = sorted(df["STT"].dropna().unique())

color_list = [
    "red", "blue", "green", "purple", "orange",
    "darkred", "lightred", "beige", "darkblue",
    "darkgreen", "cadetblue", "darkpurple", "pink",
    "lightblue", "lightgreen", "gray", "black"
]

stt_color_map = {
    stt: color_list[i % len(color_list)]
    for i, stt in enumerate(unique_stt)
}

# Tạo bản đồ
m = folium.Map(
    location=[df["lat"].mean(), df["lon"].mean()],
    zoom_start=10
)
Fullscreen(position="topright").add_to(m)

# Vẽ các điểm
for _, row in df.iterrows():
    stt = row["STT"]
    color = stt_color_map.get(stt, "gray")

    tooltip_text = f"""
    Tên cơ sở: {row['Tên cơ sở']}
    Số BN: {row['Số BN']}
    """

    popup_text = f"""
    <b>{row['Tên cơ sở']}</b><br>
    STT: {row['STT']}<br>
    Địa chỉ: {row['Địa chỉ']}<br>
    Điện thoại: {row['Điện thoại liên hệ']}<br>
    Số BN: {row['Số BN']}
    """

    folium.Marker(
        location=[row["lat"], row["lon"]],
        tooltip=tooltip_text,
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color=color)
    ).add_to(m)

# Hiển thị bản đồ
st_folium(m, use_container_width=True, height=800)

# Chú giải màu theo STT
st.subheader("Chú giải màu theo STT")
legend_df = pd.DataFrame({
    "STT": list(stt_color_map.keys()),
    "Màu": list(stt_color_map.values())
})
st.dataframe(legend_df, use_container_width=True)
