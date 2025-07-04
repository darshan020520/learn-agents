# main.py
from agent import memory_wrapped_executor
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
import asyncio


async def run_agent(user_input: str, session_id: str):
    token_callback = AsyncIteratorCallbackHandler()
    steps_queue = asyncio.Queue()
        
    try:
        async def emit_step(action, observation):
            await steps_queue.put({
                "type": "step",
                "tool": action.tool,
                "tool_input": action.tool_input,
                "log": action.log,
                "observation": observation
            })
        # Run the agent
        task = asyncio.create_task(memory_wrapped_executor.ainvoke(
            {"input": user_input},
            config={
                "callbacks": [token_callback],
                "configurable": {"session_id": session_id}
            }
        ))
        
        async for token in token_callback.aiter():
            yield {"type": "token", "value": token}

        # --- 4. Wait for final result (includes intermediate steps) ---
        final_result = await task

        # --- 5. Emit intermediate steps after agent completes ---
        for action, observation in final_result.get("intermediate_steps", []):
            await emit_step(action, observation)
            step = await steps_queue.get()
            print("Yielding step:", step)
            yield step


        # --- 6. Final fallback output (non-streamed final reply) ---
        if final_result.get("output"):
            yield {"type": "token", "value": final_result["output"]}
        
    
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Streaming error.\n")

    finally:
        # ✅ Always close the stream
        yield {"type": "__end__"}