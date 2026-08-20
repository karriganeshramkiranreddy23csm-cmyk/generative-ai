import streamlit as st
import json
from college_data import COLLEGE_DATA
from prompts import SYSTEM_PROMPT
from chatbot import get_llm_response

# Page config
st.set_page_config(page_title="College Admission Assistant", page_icon="🎓", layout="centered")

# Initialize session state for conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Initialize system prompt
    college_data_str = json.dumps(COLLEGE_DATA, indent=2)
    sys_prompt = SYSTEM_PROMPT.format(
        college_name=COLLEGE_DATA["college_name"],
        college_data=college_data_str
    )
    st.session_state.messages.append({"role": "system", "content": sys_prompt})

# Sidebar
with st.sidebar:
    st.title("🎓 College Admission Assistant")
    st.markdown("""
    **About**
    Ask questions about:
    • Courses
    • Eligibility
    • Fees
    • Admission procedure
    • Documents
    • General admission information
    """)
    st.divider()
    st.markdown("⚙️ **Settings**")
    st.markdown("Model: `openai/gpt-oss-20b`\nTemperature: `0.3`")
    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        # Reset messages, keeping only the system prompt
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

    st.divider()
    st.markdown("💡 **Try asking:**")
    st.markdown("""
    • What courses are offered?
    • What is the eligibility for B.Tech Computer Science?
    • What is the fee for BCA?
    • What documents are required?
    • How can I apply?
    """)

# Main UI Header
st.title("🎓 College Admission Assistant")
st.subheader("Your AI-powered admission guide")

# Display experiment details
with st.expander("🔬 Experiment Details"):
    st.markdown("""
    **Model:** openai/gpt-oss-20b
    **Prompt Engineering:** Role-based prompting, Context Injection (RAG-lite), Constraint Rules.
    **Memory:** `st.session_state`
    """)
    st.write(f"**Total Conversation Messages:** {len(st.session_state.messages)}")
    if len(st.session_state.messages) > 1:
        st.json(st.session_state.messages[1:])
    else:
        st.write("No conversation yet.")

# Display chat history (excluding system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = "🤖" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your question here..."):
    # Immediately display the user's message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Store user message in conversation history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate assistant response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            response = get_llm_response(st.session_state.messages)
            st.markdown(response)
            
    # Store assistant response in conversation history
    st.session_state.messages.append({"role": "assistant", "content": response})
