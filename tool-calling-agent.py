import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()  # now picks it up from .env


# Pre-defined tools for the agent
def search_docs(query: str) -> str:
    docs = {
        "recursive": "Recursive is an AI consulting company in Tokyo, founded 2020.",
        "tokyo": "Tokyo is the capital of Japan, population ~14 million.",
        "japan": "Japan is an island country in East Asia, known for its technology and culture.",
    }
    matches = [v for k, v in docs.items() if k in query.lower()]
    return "\n".join(matches) if matches else "No matching documents."


def get_weather(city: str) -> str:
    weather = {"tokyo": "18°C, partly cloudy", "osaka": "20°C, sunny"}
    return weather.get(city.lower(), f"No weather for {city}")


TOOLS_SCHEMA = [
    {
        "name": "search_docs",
        "description": "Search internal documents by keyword.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
]

TOOLS = {"search_docs": search_docs, "get_weather": get_weather}


def run_agent(user_message: str, max_iterations: int = 8) -> str:
    """Run the agent loop until model produces a final answer or max iterations.
    
    Requirements:
    - Maintain message history including assistant tool-call messages and tool results
    - Dispatch each tool call, append the result with role="tool"
    - If model calls an unknown tool, return a helpful error to the model and continue
    - If a tool raises, return the error to the model and continue (don't crash the agent)
    - Cap iterations to prevent runaway loops
    """
    messages = [{'role': 'user', 'content': user_message}]

    for _ in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            tools=TOOLS_SCHEMA,
            messages=messages,
        )

        # if done, we return the text answer
        if response.stop_reason == "end_turn":
            return next((b.text for b in response.content if hasattr(b, "text")), "")

                         
        # append the assistant message to history
        messages.append({"role": "assistant", "content": response.content})

        # run each tool and collect the results
        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            tools_func = TOOLS.get(block.name)
            if tools_func is None:
                result = f"Error: Unknown tool '{block.name}'"
            else:
                try:
                    result = tools_func(**block.input)
                except Exception as e:
                    result = f"Error running tool '{block.name}': {str(e)}"

            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})

        # append tool results to history
        messages.append({"role": "user", "content": tool_results})

    return "Max iterations reached without a final answer."

if __name__ == "__main__":
    print(run_agent("What's the weather in Tokyo and what is Recursive?"))