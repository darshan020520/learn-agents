import streamlit as st
from main import run_agent
import uuid
from agent import chat_map
import asyncio

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.title('Weather tool')

user_input = st.text_input('Enter your question:')

if st.button('Submit') and user_input:
    history = chat_map.get(st.session_state.session_id)
    if history:
        st.markdown("### 🗂️ Conversation History")
        for i, msg in enumerate(history.messages):
            role = "👤 You" if msg.type == "human" else "🤖 Assistant"
            st.chat_message(role).write(msg.content)
    
    with st.spinner("Thinking..."):
        response_placeholder = st.empty()
        final_response = [""]  # outer scope variable

        async def stream_response():
            async for token in run_agent(user_input, st.session_state.session_id):
                final_response[0] += token
                response_placeholder.markdown(final_response[0])
        
        asyncio.run(stream_response())

    # if steps:
    #     st.markdown("**Steps:**")
    #     for i, (action, observation) in enumerate(steps):
    #         with st.expander(f"🔁 Step {i+1}: {action.tool}", expanded=False):
    #             st.markdown("**🧠 Reasoning**")
    #             st.code(action.log.strip() or "[No reasoning log]", language="markdown")

    #             st.markdown("**📥 Tool Input**")
    #             st.json(action.tool_input)

    #             st.markdown("**📤 Tool Output**")
    #             st.json(observation if isinstance(observation, dict) else {"result": observation})