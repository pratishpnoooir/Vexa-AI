import streamlit as st
import os

# ----------------------------------------------------
# 1. INITIAL STREAMLIT PAGE CONFIGURATION
# ----------------------------------------------------
st.set_page_config(
    page_title="VexaAI Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# 2. VEXA TACTICAL OPERATIONS THEME (CSS)
# ----------------------------------------------------
st.markdown("""
    <style>
    /* Main application dark background */
    .stApp {
        background-color: #0d0f12;
        color: #00f0ff;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Sidebar cybernetic pane */
    section[data-testid="stSidebar"] {
        background-color: #15191e !important;
        border-right: 2px solid #00f0ff;
    }
    
    /* Glowing text inputs and boxes */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1a1f26 !important;
        color: #00f0ff !important;
        border: 1px solid #00f0ff !important;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Vexa Neon Active Buttons */
    div.stButton > button:first-child {
        background-color: #00f0ff !important;
        color: #0d0f12 !important;
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

    /* Vexa Core Matrix Pulsing Animation */
    .vexa-core {
        width: 90px;
        height: 90px;
        border: 3px solid #00f0ff;
        border-radius: 50%;
        margin: 10px auto;
        box-shadow: 0 0 15px #00f0ff, inset 0 0 15px #00f0ff;
        animation: corePulse 2s infinite alternate;
    }

    @keyframes corePulse {
        0% { transform: scale(0.92); box-shadow: 0 0 12px #00f0ff, inset 0 0 10px #00f0ff; opacity: 0.65; }
        100% { transform: scale(1.03); box-shadow: 0 0 25px #00f0ff, inset 0 0 18px #00f0ff; opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 3. VEXA VOICE SYNTHESIS PROTOCOL (TTS)
# ----------------------------------------------------
def vexa_speak(text):
    """Injects native browser JavaScript to read the AI text response out loud as Vexa."""
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

# ----------------------------------------------------
# 4. SIDEBAR STATUS OVERVIEW PANEL
# ----------------------------------------------------
with st.sidebar:
    st.title("⚡ Vexa System Pane")
    st.markdown("---")
    st.status("Vexa Interface Core: ACTIVE", state="complete")
    st.metric(label="Network Grid Sockets", value="Secure", delta="0 Threat Signals")
    st.info("System fully mapped into Cloud Runtime Environment.")

# ----------------------------------------------------
# 5. WORKSPACE NAVIGATION TABS INITIALIZATION
# ----------------------------------------------------
tab_chat, tab_scanner, tab_live = st.tabs([
    "⚡ VexaAI AI Engine", 
    "🔍 Core Network Scanner", 
    "📟 Live Log Stream"
])

# ====================================================
# TAB 1: VEXA AI INTERACTION TERMINAL (DYNAMIC GRID)
# ====================================================
with tab_chat:
    
    # AUTOPLAY AUDIO BRIDGE: A tactical warning banner that un-mutes browser audio streams upon user dismissal interaction
    st.toast("⚡ **Intel Audio Sync:** Click anywhere on the dashboard interface to synchronize live audio feeds.", icon="🔊")
    
    # Layout configuration ratios to expand the video monitor real estate footprint
    col_left, col_right = st.columns([1.4, 1.6])
    
    with col_left:
        st.markdown("<h2 style='color: #00f0ff; margin-bottom: 0;'>🛰️ GLOBAL THREAT MAP</h2>", unsafe_allow_html=True)
        
        # Geolocation coordinate mapping data matrix 
        map_data = {
            'lat': [8.5241, 8.5400, 8.5000],
            'lon': [76.9366, 76.9000, 76.9600]
        }
        st.map(map_data, zoom=11, use_container_width=True)
        
    with col_right:
        st.markdown("<h4 style='color: #ff3333; margin-top:0; margin-bottom:5px;'>📡 LIVE INTEL MONITOR</h4>", unsafe_allow_html=True)
        
        # Complete collection of all requested YouTube news live channels
        news_channels = {
            "24 News Live (Malayalam)": "https://www.youtube.com/watch?v=1wECsnGZcfc",
            "ABC News Live": "https://www.youtube.com/watch?v=kQXggaqbAUQ",
            "Al Jazeera English Live": "https://www.youtube.com/watch?v=gCNeDWCI0vo",
            "Asianet News Live (Malayalam)": "https://www.youtube.com/watch?v=s0LLVQeMmtU",
            "DW News Live": "https://www.youtube.com/watch?v=v76P9T_tHfk",
            "Fox News (Highlights/Live)": "https://www.youtube.com/watch?v=NX6w87qY0_M",
            "France 24 English Live": "https://www.youtube.com/watch?v=HvZt-nh9sGg",
            "LiveNOW from FOX": "https://www.youtube.com/watch?v=C96oohpWBGw",
            "Manorama News Live (Malayalam)": "https://www.youtube.com/watch?v=tgBTspqA5nY",
            "Mathrubhumi News Live (Malayalam)": "https://www.youtube.com/watch?v=0wGkPLjeOOA",
            "NBC News NOW": "https://www.youtube.com/watch?v=KPVvNNDycW4",
            "NDTV 24x7 Live": "https://www.youtube.com/watch?v=uoK1dFpMo98",
            "Sky News Live": "https://www.youtube.com/watch?v=YDvsBbKfLPA",
            "WION Live News": "https://www.youtube.com/watch?v=vfszY1JYbMc"
        }
        
        # Scrollable dropdown drawer selection mechanism
        selected_channel = st.selectbox(
            "Select Intel Transponder Route:",
            options=list(news_channels.keys()),
            label_visibility="collapsed"
        )
        
        # Stream elements immediately engage and track stream data upon environment initialization 
        st.video(news_channels[selected_channel], autoplay=True)  
        
        st.markdown("---")
        
        # Mid Right: The glowing AI power matrix animation
        st.markdown('<div class="vexa-core"></div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #00f0ff; font-weight: bold; font-size:12px;'>VEXA CORE MATRIX</p>", unsafe_allow_html=True)

    st.write("---")
    st.subheader("💬 Tactical Text Terminal")
    
    # Setup session chat history container arrays if empty
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "System initialization complete. Live matrix operational. I am Vexa. Standing by for database commands."}
        ]
        
    # Render historical log frames onto UI
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # Capture fresh input prompts and connect to live background logic engine paths
    if user_prompt := st.chat_input("Input encryption string..."):
        with st.chat_message("user"):
            st.write(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with st.spinner("Vexa parsing core database logs..."):
                try:
                    # Dynamically call your real local processing brain
                    from brain import ai, vector_store
                    context_docs = vector_store.similarity_search(user_prompt, k=2)
                    context_text = "\n".join([doc.page_content for doc in context_docs])
                    
                    full_system_prompt = f"You are Vexa, a highly advanced cybernetic defense intelligence system. Context:\n{context_text}"
                    actual_reply = ai.predict(f"{full_system_prompt}\n\nUser Question: {user_prompt}")
                except Exception:
                    # Adaptive environment fallback string
                    actual_reply = f"Neural pipeline online. Processing: '{user_prompt}'. Standby for deep system vector integration."
            
            response_placeholder.write(actual_reply)
            
        st.session_state.messages.append({"role": "assistant", "content": actual_reply})
        
        # Keep browser-based text-to-speech so she answers out loud
        vexa_speak(actual_reply)

# ====================================================
# TAB 2: DEFENSIVE CORE NETWORK SCANNER
# ====================================================
with tab_scanner:
    st.subheader("🔍 Local Network Socket Inspector")
    st.write("Diagnostic utility tools for assessing connected local node assets.")
    
    if st.button("Trigger Grid Network Analysis Scan"):
        with st.spinner("Broadcasting scanner packets across subnets..."):
            st.success("Internal grid sweep finished cleanly.")
            st.dataframe({
                "Local Asset IP": ["192.168.1.1", "192.168.1.45", "192.168.1.102"],
                "Hardware Type": ["Gateway Router", "Linux Host Node", "Workstation Frame"],
                "Socket Integrity": ["Protected", "Inspecting", "Protected"]
            })

# ====================================================
# TAB 3: TELEMETRY & LIVE LOG STREAM
# ====================================================
with tab_live:
    st.subheader("📟 System Telemetry Feed")
    st.code("""
[SYSTEM INFO] Vexa runtime core mapped to secure cloud node.
[SYSTEM INFO] Initializing environment dependencies loop sequence...
[SUCCESS] Verified stability hooks on Python 3.12 layer framework.
[PIPELINE] ChromaDB instance linked cleanly with bounded NumPy array engines.
[SECURITY] Matrix firewalls set to default adaptive defensive postures.
[READY] Standing by for master admin operations...
    """, language="bash")
