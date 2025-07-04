import streamlit as st
from main import run_agent
import uuid
from agent import chat_map
import asyncio
from langchain_core.chat_history import InMemoryChatMessageHistory

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
        steps_container = st.container()
        final_response = [""]

        async def stream_response():
            async for chunk in run_agent(user_input, st.session_state.session_id):
                if isinstance(chunk, str):
                    continue  # protect against unstructured raw strings

                if chunk.get("type") == "token":
                    final_response[0] += chunk["value"]
                    response_placeholder.markdown(final_response[0])

                elif chunk.get("type") == "step":
                    with st.expander(f"🧠 Intermediate Step – Tool: {chunk['tool']}", expanded=False):
                        st.markdown("**🧠 Reasoning**")
                        st.code(chunk["log"].strip() or "[No reasoning log]", language="markdown")

                        st.markdown("**📥 Tool Input**")
                        st.json(chunk["tool_input"])

                        st.markdown("**📤 Tool Output**")
                        st.json(chunk["observation"] if isinstance(chunk["observation"], dict) else {"result": chunk["observation"]})

                elif chunk == "__end__":
                    break


        asyncio.run(stream_response())

if st.button("Debug: Show All Sessions"):
    st.json({
        "Total Sessions": len(chat_map),
        "Current Session": st.session_state.session_id,
        "Session Exists": st.session_state.session_id in chat_map,
        "Message Count": len(chat_map.get(st.session_state.session_id, InMemoryChatMessageHistory()).messages) if st.session_state.session_id in chat_map else 0
    })

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