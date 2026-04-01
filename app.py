import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen

st.set_page_config(layout="wide")

file_path = "dieu tri.xlsx"
df = pd.read_excel(file_path)

df.columns = df.columns.str.strip()
df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
df["Số BN"] = pd.to_numeric(df["Số BN"], errors="coerce")
df = df.dropna(subset=["lat", "lon"])

st.title("Bản đồ cơ sở điều trị")

# Đỏ nhạt -> đỏ đậm theo Số BN
def get_red_color(so_bn):
    if pd.isna(so_bn):
        return "#bdbdbd"   # xám nếu thiếu dữ liệu
    elif so_bn < 100:
        return "#fee5d9"
    elif so_bn < 500:
        return "#fcae91"
    elif so_bn < 1000:
        return "#fb6a4a"
    else:
        return "#cb181d"

# Tăng nhẹ kích thước theo Số BN
def get_radius(so_bn):
    if pd.isna(so_bn):
        return 5
    elif so_bn < 100:
        return 6
    elif so_bn < 500:
        return 8
    elif so_bn < 1000:
        return 10
    else:
        return 12

m = folium.Map(
    location=[df["lat"].mean(), df["lon"].mean()],
    zoom_start=10
)
Fullscreen(position="topright").add_to(m)

for _, row in df.iterrows():
    so_bn = row["Số BN"]
    color = get_red_color(so_bn)
    radius = get_radius(so_bn)

    tooltip_text = (
        f"{row['Tên cơ sở']}<br>"
        f"Số BN: {int(so_bn) if pd.notna(so_bn) else 'Không có dữ liệu'}"
    )

    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.85,
        tooltip=folium.Tooltip(tooltip_text, sticky=True)
    ).add_to(m)

st_folium(m, use_container_width=True, height=800)

st.subheader("Chú giải màu theo số bệnh nhân")
legend_df = pd.DataFrame({
    "Nhóm số BN": ["< 100", "100 - < 500", "500 - < 1000", ">= 1000"],
    "Màu": ["đỏ rất nhạt", "đỏ nhạt", "đỏ vừa", "đỏ đậm"]
})
st.dataframe(legend_df, use_container_width=True)
