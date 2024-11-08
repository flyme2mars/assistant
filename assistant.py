# type: ignore
from youtube_downloader import youtube_downloader
from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

MODEL_NAME = "grok-beta"
XAI_API_KEY = os.getenv("XAI_API_KEY")

functions = [
    {
        "name": "youtube_downloader",
        "description": "Downloads a YouTube video with best quality to the 'downloads' folder",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "YouTube video URL",
                    "example_value": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                },
                "filename": {
                    "type": "string",
                    "description": "Desired filename for the video (without extension)",
                    "example_value": "my_video",
                },
            },
            "required": ["url", "filename"],
            "optional": [],
        },
    },
]


client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)


tools = [{"type": "function", "function": f} for f in functions]


def chat_with_tools():
    messages = [
        {
            "role": "system",
            "content": "You are a helpful tool assistant. Use the supplied tools to assist the user.",
        },
    ]

    while True:
        user_input = input("\nEnter your question (or 'quit' to exit): ")

        if user_input.lower() == "quit":
            break

        messages.append({"role": "user", "content": user_input})

        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools,
                stream=True,
            )

            print("\nAssistant:", end=" ")
            response_chunks = []
            for chunk in completion:
                if (
                    hasattr(chunk.choices[0].delta, "content")
                    and chunk.choices[0].delta.content
                ):
                    content = chunk.choices[0].delta.content
                    print(content, end="")
                    response_chunks.append(content)

                if hasattr(chunk.choices[0].delta, "tool_calls"):
                    tool_calls = chunk.choices[0].delta.tool_calls
                    if tool_calls:
                        for tool_call in tool_calls:
                            if tool_call.function.name == "youtube_downloader":
                                args = json.loads(tool_call.function.arguments)
                                result = youtube_downloader(
                                    args["url"], args["filename"]
                                )
                                messages.append(
                                    {
                                        "role": "assistant",
                                        "content": "",
                                        "tool_calls": [
                                            {
                                                "id": tool_call.id,
                                                "type": "function",
                                                "function": {
                                                    "name": tool_call.function.name,
                                                    "arguments": tool_call.function.arguments,
                                                },
                                            }
                                        ],
                                    }
                                )
                                messages.append(
                                    {
                                        "role": "tool",
                                        "content": str(result),
                                        "tool_call_id": tool_call.id,
                                    }
                                )
            print()

            if response_chunks:
                messages.append(
                    {"role": "assistant", "content": "".join(response_chunks)}
                )

        except Exception as e:
            print(f"\nError occurred: {str(e)}")
            messages = [messages[0]]


if __name__ == "__main__":
    chat_with_tools()
