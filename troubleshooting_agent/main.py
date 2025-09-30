import streamlit as st
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from app.agent_logic import build_graph

st.set_page_config(page_title="NetFix", page_icon="💬")
st.header("NetFix: Your Troubleshooter Pal 🛠️")

# Build the agent graph once
try:
    if "rag_agent" not in st.session_state:
        st.session_state.rag_agent = build_graph()
except Exception as e:
    st.error(f"Error initializing the agent: {e}")
    st.stop()

# Initialize session state for the conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [AIMessage(content="Hello! How can I help you?")]

# Display existing messages in the chat
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    else:
        st.chat_message("assistant").write(msg.content)

# Handle new user input
if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    # Invoke the agent
    with st.spinner("Thinking..."):
        try:
            response = st.session_state.rag_agent.invoke({"messages": st.session_state.messages})
            response_content = response['messages'][-1].content
        except Exception as e:
            response_content = f"An error occurred: {e}"
            st.error(response_content)

    # Add agent response to session state and display
    st.session_state.messages.append(AIMessage(content=response_content))
    st.chat_message("assistant").write(response_content)