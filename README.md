# AI Agent System - Phase 1

I've been building an AI agent that can actually do things in the real world - not just chat, but use tools to get real information. This is the first phase where I got the core system working with some basic tools.

## What it does

The agent can:
- Figure out where you are (using your IP)
- Get weather info for any city
- Convert between currencies with live rates
- Remember your conversation history
- Show you exactly how it thinks (step by step)

## How to run it

1. **Install stuff:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add your OpenAI key:**
   Create a `.env` file and put:
   ```
   OPENAI_API_KEY=your_key_here
   ```

3. **Start the web app:**
   ```bash
   streamlit run prompt_ui.py
   ```

## What's in the code

- `agent.py` - The main agent brain with memory
- `tools.py` - The actual tools it can use (weather, location, currency)
- `main.py` - Handles streaming responses
- `prompt_ui.py` - The web interface
- `debug_main.py` - For when you want to see what's happening under the hood

## Try these questions

- "What's the weather where I am right now?"
- "Convert 50 dollars to euros"
- "What's the weather like in Tokyo?"
- "Where am I located?"

## Cool features

The web interface shows you exactly what the agent is thinking - you can expand each step to see:
- Why it chose to use a particular tool
- What data it sent to the tool
- What the tool sent back

It also remembers your conversation, so you can ask follow-up questions.

## What's next

This is just phase 1. I'm planning to add more tools, maybe some web search capabilities, and probably make it faster. But for now, it's a solid foundation that actually works!

---

*Built with LangChain and OpenAI's GPT-4. Weather data from wttr.in, location from ip-api.com, and exchange rates from exchangerate-api.com.*
