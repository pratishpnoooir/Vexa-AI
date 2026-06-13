import os
from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

print("⚡ Initializing VexaAI Core Protocols...")


if not os.path.exists('./knowledge'):
    os.makedirs('./knowledge')


if not os.listdir('./knowledge'):
    print("💾 Primary memory bank empty. Writing VexaAI baseline data...")
    with open('./knowledge/vexa_core.txt', 'w') as f:
        f.write(
            "VexaAI is an independent, offline defense and automation assistant initialized in 2026. "
            "The master security analyst access code is Alpha-992. "
            "VexaAI operates locally within an isolated sandbox environment with zero cloud dependency."
        )
    print("✅ Baseline core data written successfully.")


loader = DirectoryLoader('./knowledge', glob="*.txt", loader_cls=TextLoader)
documents = loader.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1500, chunk_overlap = 150)
docs = text_splitter.split_documents(documents)

print("🧠 Loading local translation matrices (CPU Mode)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


vector_store = Chroma.from_documents(docs, embeddings)

retriever = vector_store.as_retriever(search_kwargs={"k":10})
print("🛡️  VexaAI Local Knowledge Base: ACTIVE")


try:
    ai = OllamaLLM(model="gemma2:2b")
except Exception as e:
    print(f"❌ Connection failed. Ensure Ollama is running background processes! Error: {e}")
    exit()


print("\n==================================================")
print("🤖 VEXAAI SYSTEM ONLINE // SECURE LOCAL CHAT LOOP")
print("   Type 'exit' or use Ctrl+C to terminate session.")
print("==================================================")
if __name__ == "__main__":
    while True:
        user_question = input("\n[VexaAI-Input] > ")
        if user_question.lower() == 'exit':
            print("\n⚡ Terminating VexaAI core instance. Goodbye.")
            break
        if not user_question.strip():
            continue
    
        matching_docs = vector_store.similarity_search(user_question, k=10)
        context = "\n---\n".join([doc.page_content for doc in matching_docs])
    
    
    full_prompt = f"""You are VexaAI, a secure, private custom assistant. 
You are a tier-1 SOC Security Analyst assistant. Answer the user's inquiry based on the security logs and network data provided in the context below. If the information requested is completely missing from the logs, state that the data was not found in the local memory banks, but perform a full analysis on any related security events present.
Context:
{context}

Question: {user_question}
Answer:"""
    
    print("\n[VexaAI-Thinking...]")
    try:
        response = ai.invoke(full_prompt)
        print(f"VexaAI: {response}")
    except Exception as e:
        print(f"❌ Processing Error: {e}")
