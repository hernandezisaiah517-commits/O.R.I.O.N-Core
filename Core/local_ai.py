import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


CHAT_URL = "http://127.0.0.1:11434/api/chat"


def generate_reply(prompt, model, assistant_name, history=None):
    if not prompt.strip():
        return "Usage: ask Your question goes here"

    if history is None:
        history = []

    system_message = {
        "role": "system",
        "content": (
            f"You are {assistant_name}, a personal assistant. "
            "Give clear, practical answers. "
            "Use the supplied conversation history for follow-up questions. "
            "Do not claim access to files, saved notes, live system "
            "status, devices, or tools."
        ),
    }

    user_message = {
        "role": "user",
        "content": f"{prompt}\n/no_think",
    }

    payload = {
        "model": model,
        "messages": [system_message] + history + [user_message],
        "stream": False,
        "think": False,
    }

    body = json.dumps(payload).encode("utf-8")

    request = Request(
        CHAT_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise ValueError(
            f"Ollama returned HTTP {error.code}. "
            "Check that the configured model appears in ollama list."
        ) from error
    except URLError as error:
        raise ValueError(
            "Could not reach local Ollama. "
            "Make sure the Ollama application is running."
        ) from error
    except TimeoutError as error:
        raise ValueError(
            "The local model took too long to respond. "
            "Try a shorter question or a smaller model."
        ) from error

    if not isinstance(result, dict):
        raise ValueError("Ollama returned an unexpected response.")

    message = result.get("message")

    if not isinstance(message, dict):
        raise ValueError("Ollama did not return an assistant message.")

    answer = message.get("content")

    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("The local model returned an empty answer.")

    if "</think>" in answer:
        answer = answer.split("</think>", 1)[1]

    if "<think>" in answer:
        raise ValueError("The model returned an incomplete reasoning block.")

    answer = answer.strip()

    if not answer:
        raise ValueError("The model returned no final answer.")

    return answer