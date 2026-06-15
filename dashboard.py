import streamlit as st

# Check if authentication is even enabled/available
if hasattr(st, "user"):
    if not st.user.is_logged_in:
        st.title("⚡ VexaAI Access Restricted")
        if st.button("Authenticate via Google"): 
            st.login("google")
        st.stop()
else:
    # Fallback for local development or environments without auth enabled
    st.sidebar.info("Developer Mode: Authentication Disabled")




import os, socket, ipaddress, hashlib, feedparser, requests, pandas as pd
import pydeck as pdk
import subprocess, platform

# ====================================================
# 1. INITIAL SYSTEM & CONFIGURATION
# ====================================================
st.set_page_config(page_title="VexaAI Command Center", page_icon="⚡", layout="wide")

# --- AUTH GATE ---
if not st.user.is_logged_in:
    st.title("⚡ VexaAI Access Restricted")
    if st.button("Authenticate via Google"): st.login("google")
    st.stop()

# ====================================================
# 2. VEXA THEME ENGINE (Your CSS)
# ====================================================
st.markdown("""
    <style>
    .stApp { background-color: #0d0f12; color: #00f0ff; font-family: 'Courier New', monospace; }
    section[data-testid="stSidebar"] { background-color: #15191e !important; border-right: 2px solid #00f0ff; }
    .stTextInput>div>div>input { background-color: #1a1f26 !important; color: #00f0ff !important; border: 1px solid #00f0ff !important; }
    div.stButton > button:first-child { background-color: #00f0ff !important; color: #0d0d12 !important; font-weight: bold; }
    .vexa-core { width: 90px; height: 90px; border: 3px solid #00f0ff; border-radius: 50%; margin: 15px auto; box-shadow: 0 0 15px #00f0ff; animation: corePulse 2s infinite alternate; }
    @keyframes corePulse { 0% { transform: scale(0.92); opacity: 0.65; } 100% { transform: scale(1.03); opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# ====================================================
# 3. FUNCTIONAL LOGIC MODULES
# ====================================================
def vexa_speak(text):
    clean = text.replace('"', '\\"').replace('\n', ' ')
    st.markdown(f'<script>var msg = new SpeechSynthesisUtterance("{clean}"); window.speechSynthesis.speak(msg);</script>', unsafe_allow_html=True)

def ping_host(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    return subprocess.call(['ping', param, '1', host]) == 0

def get_weather():
    try:
        data = requests.get("https://api.open-meteo.com/v1/forecast?latitude=8.5241&longitude=76.9366&current=temperature_2m,wind_speed_10m").json()['current']
        return f"{data['temperature_2m']}°C, Wind: {data['wind_speed_10m']}km/h"
    except: return "Telemetry Offline"

# ====================================================
# 4. TABS INTEGRATION
# ====================================================
tab_chat, tab_ctf, tab_scanner, tab_crypto, tab_intel, tab_live = st.tabs([
    "⚡ VexaAI Engine", "🏆 Bandit Matrix", "🔍 Recon", "🔐 Crypto", "📡 Threat Intel", "📺 Live News"
])

with tab_chat:
    st.subheader("🛰️ 3D Threat Matrix")
    if st.button("Render Global Threat Matrix"):
        df = pd.DataFrame({'lat': [8.5241], 'lon': [76.9366], 'threat': [50]})
        st.pydeck_chart(pdk.Deck(initial_view_state=pdk.ViewState(lat=8.5, lon=76.9, zoom=10, pitch=50),
                                 layers=[pdk.Layer("ColumnLayer", df, get_position="[lon, lat]", get_elevation="threat", elevation_scale=1000, extruded=True)]))
    
    if prompt := st.chat_input("Command..."):
        response = f"Vexa processing: {prompt}"
        st.chat_message("assistant").write(response)
        vexa_speak(response)

with tab_scanner:
    st.subheader("🔍 Network Recon")
    target = st.text_input("Target IP:", "127.0.0.1")
    if st.button("Run Diagnostics"):
        status = "REACHABLE" if ping_host(target) else "UNREACHABLE"
        st.success(f"Status: {status}")
        open_ports = [p for p in [80, 443, 8080] if socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex((target, p)) == 0]
        st.write(f"Open Ports: {open_ports}")

with tab_intel:
    st.subheader("🌤️ Environmental Intel")
    st.metric("Trivandrum Current", get_weather())

with tab_live:
    st.subheader("📺 YouTube Live Intel")
    yt_rss = "https://www.youtube.com/feeds/videos.xml?channel_id=UC_x5XG1OV2P6uZZ5FSM9Ttw"
    for entry in feedparser.parse(yt_rss).entries[:3]:
        st.video(entry.link)
        st.write(entry.title)
