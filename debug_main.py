# main_debug.py
from agent import agent_executor, show_scratchpad
import json

def debug_query(query):
    print(f"\n{'#'*80}")
    print(f"PROCESSING QUERY: {query}")
    print(f"{'#'*80}")
    
    # Run with intermediate steps
    result = agent_executor.invoke({"input": query})
    
    # Show the scratchpad
    if 'intermediate_steps' in result:
        show_scratchpad(result['intermediate_steps'])
    
    print(f"\n{'='*60}")
    print("🎯 FINAL ANSWER")
    print(f"{'='*60}")
    print(result['output'])
    
    # Show raw result structure
    print(f"\n{'='*60}")
    print("🔍 RAW RESULT STRUCTURE")
    print(f"{'='*60}")
    print(json.dumps({
        "input": result.get('input'),
        "output": result.get('output'),
        "intermediate_steps_count": len(result.get('intermediate_steps', []))
    }, indent=2))
    
    return result

if __name__ == "__main__":
    # Test query
    query = "What's the weather at my current location?"
    
    print("🔬 DEEP DIVE AGENT DEBUGGER")
    print("Watch exactly what happens inside the agent's mind!\n")
    
    debug_query(query)
    
    # Interactive mode
    print(f"\n{'='*80}")
    print("Enter queries to debug (or 'exit' to quit):")
    
    while True:
        user_input = input("\nQuery: ").strip()
        if user_input.lower() == 'exit':
            break
        debug_query(user_input)