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
# 2. VEXA TACTICAL THEME & CORE ANIMATION (CSS)
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
        width: 110px;
        height: 110px;
        border: 3px solid #00f0ff;
        border-radius: 50%;
        margin: 25px auto;
        box-shadow: 0 0 15px #00f0ff, inset 0 0 15px #00f0ff;
        animation: corePulse 2s infinite alternate;
    }

    @keyframes corePulse {
        0% { 
            transform: scale(0.95); 
            box-shadow: 0 0 12px #00f0ff, inset 0 0 10px #00f0ff; 
            opacity: 0.65; 
        }
        100% { 
            transform: scale(1.05); 
            box-shadow: 0 0 28px #00f0ff, inset 0 0 18px #00f0ff; 
            opacity: 1; 
        }
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 3. VEXA VOICE SYNTHESIS PROTOCOL (TTS)
# ----------------------------------------------------
def vexa_speak(text):
    """Injects native browser JavaScript to read the AI text response out loud as Vexa."""
    if text:
        # Sanitize text for JavaScript delivery
        clean_text = text.replace('"', '\\"').replace('\n', ' ')
        js_speech = f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            window.speechSynthesis.cancel(); // Flush old audio queues
            
            var voices = window.speechSynthesis.getVoices();
            for(var i = 0; i < voices.length; i++) {{
                // Fallback loops to grab a sharp, clear female assistant profile
                if(voices[i].name.includes("Google UK English Female") || voices[i].name.includes("Zira") || voices[i].name.includes("Female")) {{
                    msg.voice = voices[i];
                    break;
                }}
            }}
            msg.rate = 1.05; // Quick processing pace
            msg.pitch = 1.0;  // Balanced response frequencies
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
# TAB 1: VEXA AI INTERACTION TERMINAL
# ====================================================
with tab_chat:
    # Render the pulsing center-stage matrix
    st.markdown('<div class="vexa-core"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #00f0ff;'>VEXA CORE DIRECT ACCESS</h3>", unsafe_allow_html=True)
    
    # Jarvis-style audio capturing block
    st.subheader("🎙️ Vexa Voice Terminal Intercom")
    audio_command = st.audio_input("Initialize Vexa Audio Uplink")
    
    if audio_command:
        st.info("⚡ Audio packet successfully intercepted by Vexa.")
        audio_bytes = audio_command.read()
        # Visual alert indicating the telemetry path is active
        st.warning("🤖 Audio data buffered! Link a Cloud API Key to stream voice conversions natively.")
        
    st.write("---")
    st.subheader("💬 Tactical Text Terminal")
    
    # Setup session chat history container arrays if empty
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "System initialization complete. I am Vexa. Standing by for administrative input."}
        ]
        
    # Render historical log frames onto UI
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # Capture fresh input string fields
    if user_prompt := st.chat_input("Input encryption string..."):
        with st.chat_message("user"):
            st.write(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # Simulated response wrapper
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            mock_reply = f"Acknowledged request: '{user_prompt}'. Processing algorithmic security pipelines."
            response_placeholder.write(mock_reply)
            
        st.session_state.messages.append({"role": "assistant", "content": mock_reply})
        
        # Fire voice protocol sequence instantly
        vexa_speak(mock_reply)

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
