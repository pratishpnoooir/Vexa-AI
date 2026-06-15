import streamlit as st
import socket, subprocess, platform, feedparser, requests, pandas as pd
import pydeck as pdk

# ====================================================
# 1. HARDENED CONFIGURATION & SAFE-AUTH GATE
# ====================================================
st.set_page_config(page_title="VexaAI Command Center", page_icon="⚡", layout="wide")

# This wrapper prevents the AttributeError by checking for the user object first
if hasattr(st, "user"):
    if not st.user.is_logged_in:
        st.title("⚡ VexaAI Access Restricted")
        if st.button("Authenticate via Google"): st.login("google")
        st.stop()
else:
    st.sidebar.info("System Note: Authentication layer inactive. Running in Dev Mode.")

# ====================================================
# 2. VEXA THEME ENGINE
# ====================================================
st.markdown("""
    <style>
    .stApp { background-color: #0d0f12; color: #00f0ff; font-family: 'Courier New', monospace; }
    section[data-testid="stSidebar"] { background-color: #15191e !important; border-right: 2px solid #00f0ff; }
    div.stButton > button:first-child { background-color: #00f0ff !important; color: #0d0d12 !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ====================================================
# 3. CORE LOGIC MODULES
# ====================================================
def ping_host(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    return subprocess.call(['ping', param, '1', host]) == 0

def get_weather():
    try:
        data = requests.get("https://api.open-meteo.com/v1/forecast?latitude=8.5241&longitude=76.9366&current=temperature_2m,wind_speed_10m").json()['current']
        return f"{data['temperature_2m']}°C | Wind: {data['wind_speed_10m']} km/h"
    except: return "Telemetry Offline"

# ====================================================
# 4. TABBED INTERFACE
# ====================================================
tabs = st.tabs(["⚡ AI Engine", "🛰️ 3D Matrix", "🔍 Network Recon", "🌤️ Environment", "📺 YouTube Intel"])

with tabs[0]: # AI Engine
    st.subheader("Tactical AI Terminal")
    if prompt := st.chat_input("Command..."):
        st.chat_message("assistant").write(f"Vexa analyzing: {prompt}")

with tabs[1]: # 3D Matrix
    st.subheader("🛰️ 3D Threat Matrix")
    if st.button("Initialize Map"):
        df = pd.DataFrame({'lat': [8.5241], 'lon': [76.9366], 'threat': [50]})
        st.pydeck_chart(pdk.Deck(initial_view_state=pdk.ViewState(lat=8.5, lon=76.9, zoom=10, pitch=50),
                                 layers=[pdk.Layer("ColumnLayer", df, get_position="[lon, lat]", get_elevation="threat", elevation_scale=1000, extruded=True)]))

with tabs[2]: # Network Recon
    st.subheader("🔍 Network Reconnaissance")
    target = st.text_input("Target IP:", "127.0.0.1")
    if st.button("Run Scan"):
        st.write(f"Ping: {'SUCCESS' if ping_host(target) else 'FAILED'}")
        ports = [p for p in [80, 443] if socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex((target, p)) == 0]
        st.write(f"Open Ports: {ports}")

with tabs[3]: # Environment
    st.subheader("🌤️ Environmental Data")
    st.metric("Trivandrum Telemetry", get_weather())

with tabs[4]: # News Feed
    st.subheader("📺 Live Intel Feed")
    yt_rss = "https://www.youtube.com/feeds/videos.xml?channel_id=UC_x5XG1OV2P6uZZ5FSM9Ttw"
    for entry in feedparser.parse(yt_rss).entries[:3]:
        st.video(entry.link)
