import os
import unittest
from contextlib import redirect_stdout
from io import StringIO
from types import SimpleNamespace
from unittest.mock import patch

with patch.dict(os.environ, {"API_KEY": "test-api-key"}):
    import main


class MainTests(unittest.TestCase):
    def setUp(self) -> None:
        main.history[:] = [main.SYSTEM_PROMPT]

    def test_exit_sends_message_and_preserves_history(self) -> None:
        response = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="Hello!"))]
        )
        output = StringIO()

        with (
            patch("builtins.input", side_effect=["Hi", "/exit"]),
            patch.object(main.client.chat.completions, "create", return_value=response) as create,
            redirect_stdout(output),
        ):
            main.main()

        create.assert_called_once()
        self.assertEqual(main.history[-2].get("content"), "Hi")
        self.assertEqual(main.history[-1].get("content"), "Hello!")
        self.assertIn("Hello!", output.getvalue())

    def test_reset_clears_conversation_history(self) -> None:
        response = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="Hello!"))]
        )
        output = StringIO()

        with (
            patch("builtins.input", side_effect=["Hi", "/reset", "/exit"]),
            patch.object(main.client.chat.completions, "create", return_value=response),
            redirect_stdout(output),
        ):
            main.main()

        self.assertEqual(main.history, [main.SYSTEM_PROMPT])
        self.assertIn("Memory cleared.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
