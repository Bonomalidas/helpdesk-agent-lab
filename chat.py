"""Tiny interactive CLI.  Start the mock API first:

    python -m uvicorn mock_servicenow.app:app --port 8099
    python chat.py
"""
from assistant.factory import build_assistant

if __name__ == "__main__":
    bot = build_assistant()
    print("HelpDesk assistant (Ctrl+C to quit). Logs are written to ./logs/")
    while True:
        try:
            msg = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if msg:
            print("bot>", bot.handle(msg)["answer"])
