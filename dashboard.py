import streamlit as st
import os
import socket
from datetime import datetime
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Import core assets directly from your backend engine
from brain import ai, vector_store 

# 1. Page Configuration
st.set_page_config(page_title="VexaAI Command Center v2.0", page_icon="⚡", layout="wide")

# Ensure structural directories exist locally
KNOWLEDGE_DIR = "./knowledge"
BANDIT_DIR = "./knowledge/bandit_notes"
LIVE_LOG_FILE = "./knowledge/live_system.log"

for folder in [KNOWLEDGE_DIR, BANDIT_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

if not os.path.exists(LIVE_LOG_FILE):
    with open(LIVE_LOG_FILE, "w") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Core VexaAI logging subsystem initialized locally.\n")

# --- UTILITY FUNCTIONS FOR LOG INGESTION ---
def index_text_content(text, source_name):
    """Slices and indexes text data directly into the Chroma DB."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    docs = [Document(page_content=chunk, metadata={"source": source_name}) for chunk in chunks]
    vector_store.add_documents(docs)
    return len(chunks)

# 2. Sidebar Component (System Controls & Data Feeds)
with st.sidebar:
    st.title("🛡️ VexaAI System Control")
    st.caption("Core Engineering Console | India")
    st.markdown("---")
    
    # Feature 2: Bandit Notes Ingestion Panel
    st.subheader("🏴‍☠️ Bandit CTF Training Index")
    note_title = st.text_input("Level Name (e.g., bandit2)", placeholder="bandit2")
    note_content = st.text_area("Paste Level Writeup / Flags / Notes", placeholder="Learned how to read files with spaces using './file\\ name'...")
    
    if st.button("Index CTF Note"):
        if note_title and note_content:
            file_name = f"{note_title.strip().lower()}.md"
            file_path = os.path.join(BANDIT_DIR, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(note_content)
            
            chunks_count = index_text_content(note_content, f"bandit_notes/{file_name}")
            st.success(f"✅ Indexed {chunks_count} chunks for {note_title}!")
        else:
            st.warning("Please fill in both fields.")

    st.markdown("---")
    
    # Generic File Uploader Module
    st.subheader("📤 Feed Raw Data")
    uploaded_file = st.file_uploader("Upload logs or scans", type=["txt", "log", "csv"])
    if uploaded_file is not None:
        file_path = os.path.join(KNOWLEDGE_DIR, uploaded_file.name)
        if not os.path.exists(file_path):
            with st.spinner("Indexing..."):
                file_text = uploaded_file.read().decode("utf-8", errors="ignore")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(file_text)
                chunks_count = index_text_content(file_text, uploaded_file.name)
                st.success(f"✅ Indexed {chunks_count} chunks!")

    st.markdown("---")
    st.subheader("📁 Memory Bank Architecture")
    if os.path.exists(KNOWLEDGE_DIR):
        all_files = [f for f in os.listdir(KNOWLEDGE_DIR) if os.path.isfile(os.path.join(KNOWLEDGE_DIR, f))]
        bandit_files = os.listdir(BANDIT_DIR) if os.path.exists(BANDIT_DIR) else []
        
        st.markdown(f"**Standard Memory:** `{len(all_files)} files`")
        st.markdown(f"**CTF Walkthroughs:** `{len(bandit_files)} targets`")
        if st.checkbox("Show indexed assets"):
            for f in all_files: st.caption(f"📄 {f}")
            for b in bandit_files: st.caption(f"🏴‍☠️ bandit_notes/{b}")

# 3. Main Workspace Layout (Using Tabs)
tab_chat, tab_scanner, tab_live = st.tabs(["⚡ VexaAI AI Engine", "🔍 Core Network Scanner", "📟 Live Log Stream"])

# --- TAB 1: DUAL-ENGINE AI CHATBOX ---
with tab_chat:
    st.title("⚡ VexaAI Core Intelligence")
    st.caption("Adaptive Engineering Companion & Security Analyst")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_question := st.chat_input("Ask a general question, query Bandit notes, or investigate logs..."):
        with st.chat_message("user"):
            st.markdown(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})

        with st.chat_message("assistant"):
            with st.spinner("VexaAI-Thinking..."):
                try:
                    # Semantic Router Keywords
                    sec_keywords = ["log", "ip", "vulnerability", "scan", "brute", "alert", "attack", "port", "nmap", "auth", "security", "bandit", "flag", "ctf", "compromise"]
                    needs_security_context = any(kw in user_question.lower() for kw in sec_keywords)
                    
                    if needs_security_context:
                        matching_docs = vector_store.similarity_search(user_question, k=10)
                        context = "\n---\n".join([doc.page_content for doc in matching_docs])
                        
                        full_prompt = f"""You are VexaAI, an authentic, adaptive AI collaborator with a touch of wit. Operating mode: SECURE ANALYST. Validate the user's technical troubleshooting efforts authentically, but correct any security misconceptions gently and directly—like a helpful peer.

Use the following pieces of local security context (including uploaded logs, system events, and Bandit CTF learning notes) to answer the user's inquiry. If the data isn't there, state it directly. Keep responses scannable.

Context:
{context}

Question: {user_question}
Answer:"""
                    else:
                        full_prompt = f"""You are VexaAI, an authentic, adaptive AI collaborator with a touch of wit. Operating mode: GENERAL RESEARCH. Address the user's true intent with insightful, clear, and concise responses. Act like a brilliant peer helping with daily tasks, coding, or engineering concepts. Keep it clean and engaging.

Question: {user_question}
Answer:"""

                    response = ai.invoke(full_prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    st.error(f"❌ Processing Error: {e}")

# --- TAB 2: INTERACTIVE NETWORK SCANNER WIDGET ---
with tab_scanner:
    st.title("🔍 Core Network Scanner")
    st.caption("Lightweight Python TCP Port Scanner running locally on your loopback/subnet")
    
    target_ip = st.text_input("Target IP Address", value="127.0.0.1")
    target_ip = target_ip.strip() 
    port_range = st.slider("Select Port Range", 1, 1024, (20, 100))
    
    if st.button("Execute TCP Scan"):
        st.info(f"Scanning target {target_ip} from port {port_range[0]} to {port_range[1]}...")
        open_ports = []
        
        progress_bar = st.progress(0)
        total_ports = port_range[1] - port_range[0] + 1
        
        for idx, port in enumerate(range(port_range[0], port_range[1] + 1)):
            # Update progress bar smoothly
            progress_bar.progress(int((idx + 1) / total_ports * 100))
            
            try:
                # Fast socket connection attempt
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1) 
                result = s.connect_ex((target_ip, port))
                if result == 0:
                    open_ports.append(port)
                s.close()
            except socket.gaierror:
                st.error(f"❌ Invalid IP or Hostname format: '{target_ip}'")
                break
            except Exception as e:
                st.error(f"Error scanning port {port}: {e}")
                break
            # Update progress bar smoothly
            progress_bar.progress(int((idx + 1) / total_ports * 100))
            
            # Fast socket connection attempt
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1) # Tight timeout for fast local testing
            result = s.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
            s.close()
            
        progress_bar.empty()
        
        if open_ports:
            st.success(f"Target Scan Complete! Found {len(open_ports)} open ports.")
            scan_report = f"Scan Report for {target_ip} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            for p in open_ports:
                st.warning(f"⚠️ Port {p} is OPEN")
                scan_report += f"- Port {p}: OPEN\n"
                
            # Log the findings directly into the local stream log file!
            with open(LIVE_LOG_FILE, "a") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SECURITY SCAN EXECUTED: Target {target_ip} has open ports: {open_ports}\n")
        else:
            st.info("Scan complete. No open TCP ports detected within that range.")

# --- TAB 3: LIVE TERMINAL LOG STREAM ---
with tab_live:
    st.title("📟 Live System Log Tailing")
    st.caption("Simulating an active host defense engine. Any network scans or manual injections append here instantly.")
    
    # Feature 3: Actionable Manual Injector
    st.subheader("💉 Manual Security Log Injection")
    inject_msg = st.text_input("Simulate a Security Event / Terminal Event", placeholder="Failed password for root from 192.168.1.105 port 49220 ssh2")
    
    if st.button("Inject Event Into Stream"):
        if inject_msg:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_event = f"[{timestamp}] ALERT: {inject_msg}\n"
            
            # Write to the live log file
            with open(LIVE_LOG_FILE, "a") as f:
                f.write(formatted_event)
                
            # Automatically tail and index this fresh block into Chroma on the fly
            chunks_count = index_text_content(formatted_event, "live_system.log")
            st.success(f"⚡ Event captured by defense pipeline and broken into {chunks_count} vector space vectors!")
        else:
            st.warning("Type an alert statement to simulate.")
            
    st.markdown("---")
    st.subheader("📄 Tail Viewing: `live_system.log`")
    
    if os.path.exists(LIVE_LOG_FILE):
        with open(LIVE_LOG_FILE, "r") as f:
            log_lines = f.readlines()
        
        # Display the last 15 lines like a real terminal 'tail -n 15' command
        tail_lines = "".join(log_lines[-15:])
        st.code(tail_lines, language="text")
