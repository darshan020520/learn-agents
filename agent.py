# agent.py - DETAILED DEBUG VERSION
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks.base import BaseCallbackHandler
from tools import tools
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# Load environment variables
load_dotenv()

class DetailedDebugHandler(BaseCallbackHandler):
    def __init__(self):
        self.step_count = 0
    
    def on_llm_start(self, serialized, prompts, **kwargs):
        self.step_count += 1
        print(f"\n{'='*60}")
        print(f"🧠 STEP {self.step_count}: LLM THINKING")
        print(f"{'='*60}")
        print("Prompt sent to LLM:")
        for prompt in prompts:
            print(f">>> {prompt}")
    
    def on_llm_end(self, response, **kwargs):
        print(f"\n💭 LLM Response (Human Readable):")
        print(response.generations[0][0].text)
        
        # NEW: Show the raw message structure
        print(f"\n🔍 RAW LLM Response Structure:")
        message = response.generations[0][0].message
        
        # Convert to dict to see the full structure
        if hasattr(message, 'dict'):
            raw_dict = message.dict()
            print(json.dumps(raw_dict, indent=2))
        
        # Also show tool calls if present
        if hasattr(message, 'tool_calls') and message.tool_calls:
            print(f"\n🛠️ Tool Calls Detected: {len(message.tool_calls)}")
            for i, tool_call in enumerate(message.tool_calls):
                print(f"\nTool Call {i+1}:")
                print(f"  - ID: {tool_call.get('id', 'N/A')}")
                print(f"  - Name: {tool_call.get('name', 'N/A')}")
                print(f"  - Arguments: {tool_call.get('args', 'N/A')}")

llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0,
    streaming=True,
    api_key=os.getenv("OPENAI_API_KEY"),
    callbacks=[DetailedDebugHandler()]
)

chat_map = {}

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools when needed to answer questions accurately."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

print("📋 AGENT SYSTEM PROMPT:")
print(prompt.messages[0].prompt.template)


agent = create_tool_calling_agent(llm, tools, prompt)


agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
    max_iterations=5
)

memory_wrapped_executor = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: chat_map.setdefault(session_id, InMemoryChatMessageHistory()),
    input_messages_key="input",
    history_messages_key="chat_history"
)

# Add a function to show the scratchpad
def show_scratchpad(intermediate_steps):
    print(f"\n{'='*60}")
    print("📝 AGENT SCRATCHPAD (Working Memory)")
    print(f"{'='*60}")
    
    for i, (action, observation) in enumerate(intermediate_steps):
        print(f"\nMemory Entry {i+1}:")
        print(f"  Action Taken: {action.tool}")
        print(f"  Tool Input: {action.tool_input}")
        print(f"  Reasoning: {action.log}")
        print(f"  Result: {observation}")