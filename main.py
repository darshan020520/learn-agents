# main.py
from agent import memory_wrapped_executor
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
import asyncio


async def run_agent(user_input: str, session_id: str):
    callback = AsyncIteratorCallbackHandler()
        
    try:
        # Run the agent
        result = asyncio.create_task(memory_wrapped_executor.ainvoke(
            {"input": user_input},
            config=
            {   "callbacks": [callback],
                "configurable":{"session_id":session_id}}))
        
        final_response = ""

        
        async for token in callback.aiter():
            final_response+=token
            yield token
        
        final_result=await result

        if not final_response.strip() and final_result.get("output"):
            yield final_result.get("output")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Streaming error.\n")