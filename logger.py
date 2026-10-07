import json
import os
from datetime import datetime


HISTORY_FILE = "history.json"


def load_history():
    """
    Load operation history from history.json.
    """

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_history(operation, method, input_length, output_length):
    """
    Save an encoding/obfuscation operation to history.
    """

    history = load_history()

    entry = {
        "operation": operation,
        "method": method,
        "input_length": input_length,
        "output_length": output_length,
        "timestamp": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )
    }

    history.insert(0, entry)

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )

    return entry


def clear_history():
    """
    Clear all operation history.
    """

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump([], file, indent=4)

def clear_history():

    with open("history.json", "w", encoding="utf-8") as file:
        json.dump([], file, indent=4)


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    entry = save_history(
        operation="Encode",
        method="Base64",
        input_length=20,
        output_length=28
    )

    print("\n===== HISTORY TEST =====")

    print("Operation :", entry["operation"])
    print("Method    :", entry["method"])
    print("Input     :", entry["input_length"])
    print("Output    :", entry["output_length"])
    print("Timestamp :", entry["timestamp"])

    print("\n===== SAVED HISTORY =====")

    history = load_history()

    for item in history:
        print(item)