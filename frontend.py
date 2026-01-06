import streamlit as st
import requests

st.set_page_config(page_title="Veritas | RTX 5070 Agent", layout="wide")

st.title("🛡️ Veritas: Local GraphRAG Agent")
st.caption("Powered by: Gemma 3 + Neo4j + ChromaDB + Docker")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking (Querying Graph + Vector DB)..."):
            try:
                # Call your Local Docker API
                response = requests.post("http://localhost:8080/ask", json={"query": prompt})
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data["sources"]
                    
                    st.markdown(answer)
                    
                    # Show the Engineering Stats (The "Flex")
                    with st.expander("🛠️ System Internals (Debug)"):
                        st.json(sources)
                        st.write(f"Backend Status: {response.status_code}")
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"API Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Failed: {e}. Is Docker running?")