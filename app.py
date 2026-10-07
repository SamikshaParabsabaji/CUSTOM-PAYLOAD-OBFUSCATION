from flask import Flask, render_template, request, redirect, url_for
import hashlib
import json
import os
from datetime import datetime

from encoder import (
    base64_encode,
    base64_decode,
    hex_encode,
    hex_decode,
    rot13_encode,
    rot13_decode,
    xor_encode,
    xor_decode,
    multi_layer_encode,
    multi_layer_decode
)


app = Flask(__name__)

HISTORY_FILE = "history.json"


# ==========================================================
# HISTORY FUNCTIONS
# ==========================================================

def load_history():
    """Load operation history from JSON file."""

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (json.JSONDecodeError, OSError):
        return []


def save_history(record):
    """Save a new operation record."""

    history = load_history()

    history.insert(0, record)

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)

    except OSError:
        pass


def clear_history_file():
    """Clear all history."""

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)

    except OSError:
        pass


# ==========================================================
# HOME / ENCODER
# ==========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    # ------------------------------------------------------
    # GET REQUEST
    # ------------------------------------------------------

    if request.method == "GET":
        return render_template("index.html")


    # ------------------------------------------------------
    # GET FORM DATA
    # ------------------------------------------------------

    data = request.form.get("data", "").strip()
    method = request.form.get("method", "").strip().lower()
    operation = request.form.get("operation", "").strip().lower()
    key = request.form.get("key", "")


    # ------------------------------------------------------
    # INPUT VALIDATION
    # ------------------------------------------------------

    if not data:
        return render_template(
            "index.html",
            error="Please enter some input text."
        )


    # ------------------------------------------------------
    # OPERATION VALIDATION
    # ------------------------------------------------------

    allowed_operations = [
        "encode",
        "decode"
    ]

    if operation not in allowed_operations:
        return render_template(
            "index.html",
            error="Invalid operation selected."
        )


    # ------------------------------------------------------
    # METHOD VALIDATION
    # ------------------------------------------------------

    allowed_methods = [
        "base64",
        "hex",
        "rot13",
        "xor",
        "multi"
    ]

    if method not in allowed_methods:
        return render_template(
            "index.html",
            error="Unsupported encoding method."
        )


    # ------------------------------------------------------
    # XOR KEY VALIDATION
    # ------------------------------------------------------

    if method == "xor" and not key.strip():

        return render_template(
            "index.html",
            error="XOR key is required."
        )


    # ------------------------------------------------------
    # PROCESSING
    # ------------------------------------------------------

    try:

        # ==================================================
        # BASE64
        # ==================================================

        if method == "base64":

            if operation == "encode":
                result = base64_encode(data)

            else:
                result = base64_decode(data)


        # ==================================================
        # HEX
        # ==================================================

        elif method == "hex":

            if operation == "encode":
                result = hex_encode(data)

            else:
                result = hex_decode(data)


        # ==================================================
        # ROT13
        # ==================================================

        elif method == "rot13":

            # ROT13 encode and decode use the same transformation
            result = rot13_encode(data)


        # ==================================================
        # XOR
        # ==================================================

        elif method == "xor":

            if operation == "encode":
                result = xor_encode(data, key)

            else:
                result = xor_decode(data, key)


        # ==================================================
        # MULTI-LAYER
        # ==================================================

        elif method == "multi":

            if operation == "encode":
                result = multi_layer_encode(data)

            else:
                result = multi_layer_decode(data)


        # ==================================================
        # SAFETY FALLBACK
        # ==================================================

        else:

            return render_template(
                "index.html",
                error="Unsupported method."
            )


        # --------------------------------------------------
        # CONVERT RESULT TO STRING
        # --------------------------------------------------

        result = str(result)


        # --------------------------------------------------
        # SHA-256 HASHES
        # --------------------------------------------------

        input_hash = hashlib.sha256(
            data.encode("utf-8")
        ).hexdigest()

        output_hash = hashlib.sha256(
            result.encode("utf-8")
        ).hexdigest()


        # --------------------------------------------------
        # SAVE HISTORY
        # --------------------------------------------------

        record = {
            "operation": operation,
            "method": method,
            "input_length": len(data),
            "output_length": len(result),
            "timestamp": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        }

        save_history(record)


        # --------------------------------------------------
        # RESULT PAGE
        # --------------------------------------------------

        return render_template(
            "result.html",
            operation=operation,
            method=method,
            result=result,
            input_hash=input_hash,
            output_hash=output_hash
        )


    # ======================================================
    # ERROR HANDLING
    # ======================================================

    except ValueError as error:

        return render_template(
            "index.html",
            error=str(error)
        )


    except Exception as error:

        print("Processing Error:", error)

        return render_template(
            "index.html",
            error="Unable to process the supplied input."
        )


# ==========================================================
# HISTORY
# ==========================================================

@app.route("/history")
def history():

    records = load_history()

    return render_template(
        "history.html",
        history=records,
        records=records
    )


# ==========================================================
# DELETE SINGLE HISTORY RECORD
# ==========================================================

@app.route("/delete-history/<int:index>", methods=["GET", "POST"])
def delete_history(index):

    records = load_history()

    if 0 <= index < len(records):

        records.pop(index)

        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                json.dump(records, file, indent=4)

        except OSError:
            pass

    return redirect(url_for("history"))


# ==========================================================
# CLEAR ALL HISTORY
# ==========================================================

@app.route("/clear-history", methods=["POST"])
def clear_history():

    clear_history_file()

    return redirect(url_for("history"))


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
def dashboard():

    records = load_history()

    # ------------------------------------------------------
    # TOTAL OPERATIONS
    # ------------------------------------------------------

    total_operations = len(records)


    # ------------------------------------------------------
    # ENCODE / DECODE COUNTS
    # ------------------------------------------------------

    encode_count = sum(
        1
        for item in records
        if str(item.get("operation", "")).lower() == "encode"
    )

    decode_count = sum(
        1
        for item in records
        if str(item.get("operation", "")).lower() == "decode"
    )


    # ------------------------------------------------------
    # METHOD COUNTS
    # ------------------------------------------------------

    method_counts = {}

    for item in records:

        method = str(
            item.get("method", "Unknown")
        ).upper()

        method_counts[method] = (
            method_counts.get(method, 0) + 1
        )


    # ------------------------------------------------------
    # RECENT OPERATIONS
    # ------------------------------------------------------

    recent_records = records[:5]


    # ------------------------------------------------------
    # DASHBOARD
    # ------------------------------------------------------

    return render_template(
        "dashboard.html",

        # Main values
        total_operations=total_operations,
        encode_count=encode_count,
        decode_count=decode_count,

        # Method information
        method_counts=method_counts,
        methods_used=method_counts,

        # Recent history
        recent_records=recent_records,
        records=records,
        history=records
    )


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.route("/health")
def health():

    return {
        "status": "running",
        "application": "Custom Payload Encoder",
        "mode": "Educational Text Transformation"
    }


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )