import streamlit as st
import socket
import ipaddress
import hashlib
import feedparser
import concurrent.futures
from streamlit_player import st_player
from datetime import datetime

# ==========================================
# 1. CORE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="VexaAI Command Centre", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0f12; color: #00f0ff; font-family: 'Courier New', monospace; }
    .vexa-core { width: 100px; height: 100px; border: 3px solid #00f0ff; border-radius: 50%; 
                 margin: 20px auto; box-shadow: 0 0 20px #00f0ff; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { transform: scale(0.95); opacity: 0.7; } 100% { transform: scale(1.05); opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. VEXA ENGINE FUNCTIONS
# ==========================================
def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((target, port)) == 0:
                return port
    except: pass
    return None

# ==========================================
# 3. INTERFACE ARCHITECTURE
# ==========================================
tab_chat, tab_ctf, tab_scanner, tab_crypto, tab_intel, tab_live = st.tabs([
    "⚡ VexaAI Engine", "🏆 CTF Matrix", "🔍 Network Matrix", 
    "🔐 Crypto Suite", "📡 Threat Intel", "📟 Live Feed"
])

with tab_chat:
    st.header("Vexa Operational AI")
    st.markdown('<div class="vexa-core"></div>', unsafe_allow_html=True)
    if prompt := st.chat_input("Inject Command..."):
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write("Vexa // Logic Gate Override: Analysis of " + prompt + " initiated.")

with tab_scanner:
    st.header("Network Security Matrix")
    target = st.text_input("Host Target:", "127.0.0.1")
    if st.button("Initiate Multi-Threaded Scan"):
        ports = [21, 22, 80, 443, 8080, 8443]
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(lambda p: scan_port(target, p), ports))
        for p in [r for r in results if r]:
            st.warning(f"SECURITY ALERT: Port {p} is OPEN/Vulnerable.")

with tab_crypto:
    st.header("Cryptographic Integrity Engine")
    data = st.text_area("Payload Data:")
    algo = st.selectbox("Algorithm:", ["SHA-256", "MD5"])
    if st.button("Execute Hash"):
        h = hashlib.sha256(data.encode()).hexdigest() if algo == "SHA-256" else hashlib.md5(data.encode()).hexdigest()
        st.code(f"Signature: {h}")

with tab_live:
    st.header("Live Tactical Media Feed")
    col1, col2 = st.columns(2)
    with col1:
        # Example Live Stream Embed
        st.subheader("Intel Stream: Sky News")
        st_player("https://www.youtube.com/watch?v=YDvsBbKfLPA")
    with col2:
        st.subheader("Intel Stream: WION")
        st_player("https://www.youtube.com/watch?v=vfszY1JYbMc")

with tab_intel:
    st.header("CISA Advisory Feed")
    feed = feedparser.parse("https://www.cisa.gov/cybersecurity-advisories.xml")
    for entry in feed.entries[:5]:
        with st.expander(entry.title):
            st.write(entry.summary)
            st.link_button("Details", entry.link)
