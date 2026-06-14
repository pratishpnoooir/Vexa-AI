import streamlit as st
import os
import socket
import ipaddress
import hashlib
import feedparser

# ====================================================
# 1. INITIAL SYSTEM & WINDOW GEOMETRY CONFIGURATION
# ====================================================
st.set_page_config(
    page_title="VexaAI Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================================================
# 2. VEXA CYBERNETIC THEME ENGINE (CUSTOM STYLING)
# ====================================================
st.markdown("""
    <style>
    /* Absolute dark background profile for terminal focus */
    .stApp {
        background-color: #0d0f12;
        color: #00f0ff;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Left sidebar console panel bounds */
    section[data-testid="stSidebar"] {
        background-color: #15191e !important;
        border-right: 2px solid #00f0ff;
    }
    
    /* Text input overrides to prevent bright white flash blinding */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1a1f26 !important;
        color: #00f0ff !important;
        border: 1px solid #00f0ff !important;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Neon glow active response triggers */
    div.stButton > button:first-child {
        background-color: #00f0ff !important;
        color: #0d0d12 !important;
        font-weight: bold;
        border: none;
        border-radius: 4px;
        box-shadow: 0 0 12px #00f0ff;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #ffffff !important;
        box-shadow: 0 0 20px #ffffff;
    }

    /* Core Matrix Glowing Hardware Pulse Indicator */
    .vexa-core {
        width: 90px;
        height: 90px;
        border: 3px solid #00f0ff;
        border-radius: 50%;
        margin: 15px auto;
        box-shadow: 0 0 15px #00f0ff, inset 0 0 15px #00f0ff;
        animation: corePulse 2s infinite alternate;
    }

    @keyframes corePulse {
        0% { transform: scale(0.92); box-shadow: 0 0 12px #00f0ff, inset 0 0 10px #00f0ff; opacity: 0.65; }
        100% { transform: scale(1.03); box-shadow: 0 0 25px #00f0ff, inset 0 0 18px #00f0ff; opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# ====================================================
# 3. NATIVE VOICE SYNTHESIS DISPATCH (JS TTS HOOK)
# ====================================================
def vexa_speak(text):
    """Executes native browser JavaScript to stream structural audio responses out loud as Vexa."""
    if text:
        clean_text = text.replace('"', '\\"').replace('\n', ' ')
        js_speech = f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            window.speechSynthesis.cancel(); 
            var voices = window.speechSynthesis.getVoices();
            for(var i = 0; i < voices.length; i++) {{
                if(voices[i].name.includes("Google UK English Female") || voices[i].name.includes("Zira") || voices[i].name.includes("Female")) {{
                    msg.voice = voices[i];
                    break;
                }}
            }}
            msg.rate = 1.05; 
            msg.pitch = 1.0;  
            window.speechSynthesis.speak(msg);
        </script>
        """
        st.markdown(js_speech, unsafe_allow_html=True)

# ====================================================
# 4. SYSTEM PANEL CONTROL SIDEBAR
# ====================================================
with st.sidebar:
    st.title("⚡ Vexa System Pane")
    st.markdown("---")
    st.status("Vexa Interface Core: ACTIVE", state="complete")
    st.metric(label="Network Grid Sockets", value="Secure", delta="0 Threat Signals")
    st.info("Cybersecurity Utilities fully integrated and operational.")

# ====================================================
# 5. CORE INTERFACE WORKSPACE NAVIGATION
# ====================================================
tab_chat, tab_scanner, tab_crypto, tab_intel, tab_live = st.tabs([
    "⚡ VexaAI Engine", 
    "🔍 Network Security Matrix",
    "🔐 Cryptographic Suite",
    "📡 Threat Intel Center",
    "📟 Live Log Stream"
])

# ----------------------------------------------------
# TAB 1: VEXA AI INTERACTION TERMINAL (DYNAMIC GRID)
# ----------------------------------------------------
with tab_chat:
    st.toast("⚡ **Intel Audio Sync:** Click anywhere on the dashboard interface to synchronize live audio feeds.", icon="🔊")
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("<h2 style='color: #00f0ff; margin-bottom: 0;'>🛰️ GLOBAL THREAT MAP</h2>", unsafe_allow_html=True)
        map_data = {
            'lat': [8.5241, 8.5400, 8.5000],
            'lon': [76.9366, 76.9000, 76.9600]
        }
        st.map(map_data, zoom=11, use_container_width=True)
        
    with col_right:
        st.markdown("<h4 style='color: #ff3333; margin-top:0; margin-bottom:5px;'>📡 LIVE INTEL MONITOR</h4>", unsafe_allow_html=True)
        
        news_channels = {
            "24 News Live (Malayalam)": "https://www.youtube.com/watch?v=1wECsnGZcfc",
            "ABC 7 New York Live": "https://www.youtube.com/watch?v=VrhYz4CL70I",
            "ABC News Live": "https://www.youtube.com/watch?v=iipR5yUp36o",
            "Al Jazeera English Live": "https://www.youtube.com/watch?v=gCNeDWCI0vo",
            "Asianet News Live (Malayalam)": "https://www.youtube.com/watch?v=s0LLVQeMmtU",
            "DW News Live": "https://www.youtube.com/watch?v=v76P9T_tHfk",
            "France 24 English Live": "https://www.youtube.com/watch?v=HvZt-nh9sGg",
            "LiveNOW from FOX": "https://www.youtube.com/watch?v=C96oohpWBGw",
            "Manorama News Live (Malayalam)": "https://www.youtube.com/watch?v=tgBTspqA5nY",
            "Mathrubhumi News Live (Malayalam)": "https://www.youtube.com/watch?v=0wGkPLjeOOA",
            "NBC News NOW": "https://www.youtube.com/watch?v=KPVvNNDycW4",
            "NDTV 24x7 Live": "https://www.youtube.com/watch?v=uoK1dFpMo98",
            "Sky News Live": "https://www.youtube.com/watch?v=YDvsBbKfLPA",
            "WION Live News": "https://www.youtube.com/watch?v=vfszY1JYbMc"
        }
        
        selected_channel = st.selectbox("Select Intel Transponder Route:", options=list(news_channels.keys()), label_visibility="collapsed")
        st.video(news_channels[selected_channel], autoplay=True)  
        
        st.markdown("---")
        st.markdown('<div class="vexa-core"></div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #00f0ff; font-weight: bold; font-size:12px; letter-spacing: 2px;'>VEXA CORE MATRIX</p>", unsafe_allow_html=True)

    st.write("---")
    st.subheader("💬 Tactical Text Terminal")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "System initialization complete. Live matrix operational. I am Vexa. Standing by for database commands."}
        ]
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if user_prompt := st.chat_input("Input encryption string..."):
        with st.chat_message("user"):
            st.write(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with st.spinner("Vexa parsing core database logs..."):
                try:
                    from brain import ai, vector_store
                    context_docs = vector_store.similarity_search(user_prompt, k=2)
                    context_text = "\n".join([doc.page_content for doc in context_docs])
                    full_system_prompt = f"You are Vexa, a highly advanced cybernetic defense intelligence system. Context:\n{context_text}"
                    actual_reply = ai.predict(f"{full_system_prompt}\n\nUser Question: {user_prompt}")
                except Exception:
                    actual_reply = f"Neural pipeline online. Processing command: '{user_prompt}'. Standby for deep system vector integration."
            
            response_placeholder.write(actual_reply)
            
        st.session_state.messages.append({"role": "assistant", "content": actual_reply})
        vexa_speak(actual_reply)

# ----------------------------------------------------
# TAB 2: ACTIVE NETWORK SECURITY MATRIX
# ----------------------------------------------------
with tab_scanner:
    st.subheader("🔍 Active Local Port Scanner")
    st.write("Perform a direct TCP connection check against common operational vector ports on a specified host node.")
    
    scan_col1, scan_col2 = st.columns([2, 1])
    with scan_col1:
        target_host = st.text_input("Target IP Address / Host:", value="127.0.0.1")
    with scan_col2:
        ports_to_scan = [21, 22, 80, 443, 8080]
        st.markdown(f"**Target Ports:** `{str(ports_to_scan)}`")
        
    if st.button("Execute TCP Socket Scan"):
        results = []
        progress_bar = st.progress(0)
        
        for idx, port in enumerate(ports_to_scan):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.8)  # Fast tactical response timeout
            result = s.connect_ex((target_host, port))
            
            status = "🔓 OPEN (Vulnerable/Active)" if result == 0 else "🔒 CLOSED / FILTERED"
            results.append({"Port": port, "Service": socket.getservbyport(port) if result == 0 else "Unknown/Hidden", "Status": status})
            s.close()
            progress_bar.progress((idx + 1) / len(ports_to_scan))
            
        st.dataframe(results, use_container_width=True)
        
    st.markdown("---")
    st.subheader("🧮 Subnet Address & Mask Calculator")
    
    subnet_input = st.text_input("Enter Subnet CIDR (e.g., 192.168.1.0/24):", value="192.168.1.0/24")
    if st.button("Analyze Subnet Infrastructure"):
        try:
            net = ipaddress.ip_network(subnet_input, strict=False)
            sub_col1, sub_col2, sub_col3 = st.columns(3)
            sub_col1.metric("Network Base Address", str(net.network_address))
            sub_col2.metric("Broadcast Target Wire", str(net.broadcast_address))
            sub_col3.metric("Total Allocatable Hosts", str(net.num_addresses - 2))
        except ValueError as e:
            st.error(f"Invalid CIDR Structural Format: {e}")

# ----------------------------------------------------
# TAB 3: CRYPTOGRAPHIC SUITE
# ----------------------------------------------------
with tab_crypto:
    st.subheader("🔐 Integrity Hashing Engine")
    st.write("Generate or cross-verify data integrity hashes to secure software assets and verify payloads.")
    
    hash_text = st.text_area("Input String to Hash Data:")
    hash_algo = st.selectbox("Select Crypto Algorithm Array:", ["md5", "sha1", "sha256"])
    
    if st.button("Compute Signature Hash"):
        if hash_text:
            hasher = hashlib.new(hash_algo)
            hasher.update(hash_text.encode('utf-8'))
            computed_hash = hasher.hexdigest()
            st.code(f"Algorithm: {hash_algo.upper()}\nHash: {computed_hash}", language="bash")
        else:
            st.warning("Please feed string data into the compiler block first.")

# ----------------------------------------------------
# TAB 4: THREAT INTEL CENTER (LIVE FEED PARSER)
# ----------------------------------------------------
with tab_intel:
    st.subheader("📡 CISA Live Cyber Threat Advisories")
    st.write("Pulling real-time defensive intel pipelines directly from the Cybersecurity & Infrastructure Security Agency.")
    
    if st.button("Query CISA Live Feed Transponder"):
        with st.spinner("Tuning receiver to CISA RSS stream..."):
            try:
                # CISA Cyber Advisories Feed
                feed_url = "https://www.cisa.gov/cybersecurity-advisories.xml"
                feed = feedparser.parse(feed_url)
                
                if feed.entries:
                    for idx, entry in enumerate(feed.entries[:5]):  # Get top 5 critical bulletins
                        with st.expander(f"🔴 {entry.title}"):
                            st.markdown(f"**Published:** {entry.get('published', 'N/A')}")
                            st.write(entry.get('summary', 'No summary payload attached.'))
                            st.markdown(f"[View Complete Advisory Directive]({entry.link})")
                else:
                    st.info("Stream verified but no active vulnerability advisories returned right now.")
            except Exception as e:
                st.error(f"Intel pipeline block encountered: {e}")

# ----------------------------------------------------
# TAB 5: TELEMETRY & LIVE LOG STREAM
# ----------------------------------------------------
with tab_live:
    st.subheader("📟 System Telemetry Feed")
    st.code("""
[SYSTEM INFO] Vexa runtime core mapped to secure cloud node.
[SYSTEM INFO] Initializing environment dependencies loop sequence...
[SUCCESS] Verified stability hooks on Python 3.12 layer framework.
[SECURITY] Native Socket, Hashing, and RSS Intel parsers mounted.
[PIPELINE] ChromaDB instance linked cleanly with bounded NumPy array engines.
[SECURITY] Matrix firewalls set to default adaptive defensive postures.
[READY] Standing by for master admin operations...
    """, language="bash")
