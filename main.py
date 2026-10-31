from pathlib import Path
import os

from dotenv import load_dotenv
from openai import APIStatusError, OpenAI, OpenAIError
from openai.types.chat import ChatCompletionMessageParam

load_dotenv()


def get(name, cast, default=None):
    return cast(os.environ[name]) if name in os.environ else default


client = OpenAI(
    api_key=os.environ["API_KEY"],
    base_url=os.environ.get("BASE_URL"),
    max_retries=get("MAX_RETRIES", int, 3),
)

MODEL: str = os.environ.get("MODEL", "gemini-3.8-flash")

PARAMS = {
    "temperature": get("TEMPERATURE", float, 0.5),
    "top_p": get("TOP_P", float, 0.9),
    "max_tokens": get("MAX_TOKENS", int, 1024),
    "presence_penalty": get("PRESENCE_PENALTY", float, 0.0),
    "reasoning_effort": get("REASONING_EFFORT", str, "low"),
    "timeout": get("TIMEOUT", float, 60),
}
PARAMS = {k: v for k, v in PARAMS.items() if v is not None}

prompt_file = Path("system_prompt.txt")
prompt_text = prompt_file.read_text(encoding="utf-8") if prompt_file.exists() else "You are a helpful, concise assistant."
SYSTEM_PROMPT: ChatCompletionMessageParam = {"role": "system", "content": prompt_text}

history: list[ChatCompletionMessageParam] = [SYSTEM_PROMPT]


def main() -> None:
    print("CLI Chatbot  (/reset to clear memory, /exit to quit)\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input == "/exit":
            break
        if user_input == "/reset":
            history[:] = [SYSTEM_PROMPT]
            print("Memory cleared.\n")
            continue

        history.append({"role": "user", "content": user_input})
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=history,
                **PARAMS,
            )
        except APIStatusError as error:
            history.pop()
            print(f"\n[API error {error.status_code}: {error.body or error}]\n")
            continue
        except OpenAIError as error:
            history.pop()
            print(f"\n[Error: {error}]\n")
            continue

        reply = response.choices[0].message.content or ""
        print("Bot:", reply, "\n")
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()