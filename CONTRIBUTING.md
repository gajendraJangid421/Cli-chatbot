# Contributing

Thanks for your interest in improving CLI Chatbot.

## Development setup

Follow the setup steps in [README.md](README.md), then run the checks locally:

```shell
python -m compileall -q main.py tests
python -m unittest discover -s tests -v
```

The tests mock API responses, so they do not need a real API key or network
access.

## Pull requests

- Keep changes focused and explain the user-visible behavior they affect.
- Add or update tests for behavior changes.
- Run the checks above before opening a pull request.
- Never include `.env`, API keys, or other credentials in a commit.
