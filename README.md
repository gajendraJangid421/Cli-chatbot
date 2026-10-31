# CLI Chatbot

A command-line chatbot that connects to an OpenAI-compatible chat completions
API. It keeps conversation history for the current run and can load a custom
system prompt from `system_prompt.txt`.

## Requirements

- Python 3.11 (the version checked by GitHub Actions)
- An API key for your provider

## Setup

1. Create and activate a virtual environment:

   ```shell
   python -m venv .venv
   ```

   On Windows, activate it with `.venv\Scripts\activate`. On macOS or Linux,
   use `source .venv/bin/activate`.

2. Install dependencies:

   ```shell
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and set `API_KEY` to your provider's key.
   Set `BASE_URL` if your provider uses a non-default OpenAI-compatible API
   endpoint.

4. Start the chatbot:

   ```shell
   python main.py
   ```

## Usage

- Enter a message to chat.
- Enter `/reset` to clear conversation history.
- Enter `/exit` or press Ctrl+C to quit.

The chatbot uses `system_prompt.txt` when the file exists. If it does not, a
generic assistant prompt is used.

## Configuration

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `API_KEY` | Yes | None | API key passed to the OpenAI client. |
| `BASE_URL` | No | SDK default | Base URL for an OpenAI-compatible API. |
| `MODEL` | No | `gemini-3.8-flash` | Model name sent with each request. |
| `MAX_RETRIES` | No | `3` | Maximum API request retries. |
| `TEMPERATURE` | No | `0.5` | Sampling temperature. |
| `TOP_P` | No | `0.9` | Nucleus sampling value. |
| `MAX_TOKENS` | No | `1024` | Maximum response tokens. |
| `PRESENCE_PENALTY` | No | `0.0` | Presence penalty sent to the API. |
| `REASONING_EFFORT` | No | `low` | Reasoning effort sent to compatible models. |
| `TIMEOUT` | No | `60` | Request timeout in seconds. |

## Tests

Run the standard-library unit tests with:

```shell
python -m unittest discover -s tests -v
```

Tests use a mocked API response and do not require a real API key or network
access. GitHub Actions runs the tests and checks Python syntax on pushes and
pull requests.
