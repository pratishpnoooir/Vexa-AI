import streamlit as st
import socket
import ipaddress
import hashlib
import feedparser
import concurrent.futures
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="VexaAI Command Center", layout="wide", page_icon="⚡")

# --- CUSTOM CSS ENGINE ---
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #00f0ff; font-family: 'Courier New', monospace; }
    .vexa-scanline { width: 100%; height: 2px; background: #00f0ff; box-shadow: 0 0 10px #00f0ff; animation: scan 4s linear infinite; }
    @keyframes scan { from { margin-top: 0; } to { margin-top: 50vh; } }
    div.stButton > button { background-color: #1a1f26; color: #00f0ff; border: 1px solid #00f0ff; }
    </style>
""", unsafe_allow_html=True)

# --- SECURITY LOGIC MODULES ---
def check_port(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return port if s.connect_ex((target, port)) == 0 else None

# --- SIDEBAR CONTROL ---
with st.sidebar:
    st.title("⚡ Vexa System")
    st.info(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    st.status("Security Protocols: ENCRYPTED", state="complete")
    
# --- MAIN TABS ---
tab_chat, tab_scan, tab_intel = st.tabs(["🤖 Vexa Intelligence", "🔍 Network Security", "📡 Global Threat Intel"])

with tab_scan:
    st.subheader("Multi-threaded TCP Port Scanner")
    target = st.text_input("Target Host", "127.0.0.1")
    ports = [21, 22, 23, 25, 53, 80, 443, 3306, 8080]
    
    if st.button("Execute Deep Scan"):
        with st.spinner("Analyzing target nodes..."):
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(lambda p: check_port(target, p), ports))
            
            open_ports = [p for p in results if p is not None]
            for port in open_ports:
                st.warning(f"ALERT: Port {port} is OPEN on {target}")

with tab_intel:
    st.subheader("Live Cyber Security Feeds")
    # You can add more security-focused feeds here
    feeds = {
        "CISA Advisories": "https://www.cisa.gov/cybersecurity-advisories.xml",
        "The Hacker News": "https://feeds.feedburner.com/TheHackersNews"
    }
    
    selected_feed = st.selectbox("Select Intel Source", list(feeds.keys()))
    feed = feedparser.parse(feeds[selected_feed])
    
    for entry in feed.entries[:5]:
        with st.expander(f"🔴 {entry.title}"):
            st.write(entry.summary)
            st.link_button("View Source", entry.link)

# --- VEXA AI INTERFACE ---
with tab_chat:
    st.markdown("<div class='vexa-scanline'></div>", unsafe_allow_html=True)
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Vexa Core Online. Awaiting input."}]
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if prompt := st.chat_input("Command Protocol..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            # Placeholder for your AI integration
            response = f"Vexa processing: {prompt}. Analysis complete."
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
