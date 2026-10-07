import base64
import codecs


# ==========================================
# BASE64
# ==========================================

def base64_encode(data):
    """Encode text using Base64."""

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    return base64.b64encode(
        data.encode("utf-8")
    ).decode("utf-8")


def base64_decode(data):
    """Decode Base64 text."""

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    try:
        decoded = base64.b64decode(
            data.encode("utf-8"),
            validate=True
        )

        return decoded.decode("utf-8")

    except Exception:
        raise ValueError("Invalid Base64 input.")


# ==========================================
# HEX
# ==========================================

def hex_encode(data):
    """Encode text using hexadecimal."""

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    return data.encode("utf-8").hex()


def hex_decode(data):
    """Decode hexadecimal text."""

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    try:
        decoded = bytes.fromhex(data)
        return decoded.decode("utf-8")

    except Exception:
        raise ValueError("Invalid hexadecimal input.")


# ==========================================
# ROT13
# ==========================================

def rot13_encode(data):
    """Encode text using ROT13."""

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    return codecs.encode(data, "rot_13")


def rot13_decode(data):
    """Decode ROT13 text."""

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    return codecs.decode(data, "rot_13")


# ==========================================
# XOR
# ==========================================

def xor_encode(data, key):
    """Encode text using XOR and return hexadecimal output."""

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    if not isinstance(key, str) or not key:
        raise ValueError("XOR key cannot be empty.")

    data_bytes = data.encode("utf-8")
    key_bytes = key.encode("utf-8")

    result = bytearray()

    for i, byte in enumerate(data_bytes):
        result.append(
            byte ^ key_bytes[i % len(key_bytes)]
        )

    return result.hex()


def xor_decode(data, key):
    """Decode XOR hexadecimal output."""

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    if not isinstance(key, str) or not key:
        raise ValueError("XOR key cannot be empty.")

    try:
        encoded_bytes = bytes.fromhex(data)

    except ValueError:
        raise ValueError(
            "Invalid XOR hexadecimal input."
        )

    key_bytes = key.encode("utf-8")

    result = bytearray()

    for i, byte in enumerate(encoded_bytes):
        result.append(
            byte ^ key_bytes[i % len(key_bytes)]
        )

    try:
        return result.decode("utf-8")

    except UnicodeDecodeError:
        raise ValueError(
            "Incorrect XOR key or invalid encoded data."
        )


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    original_text = "Hello Cyber Security"

    print("\n===== BASE64 =====")

    encoded = base64_encode(original_text)
    decoded = base64_decode(encoded)

    print("Original :", original_text)
    print("Encoded  :", encoded)
    print("Decoded  :", decoded)


    print("\n===== HEX =====")

    encoded = hex_encode(original_text)
    decoded = hex_decode(encoded)

    print("Original :", original_text)
    print("Encoded  :", encoded)
    print("Decoded  :", decoded)


    print("\n===== ROT13 =====")

    encoded = rot13_encode(original_text)
    decoded = rot13_decode(encoded)

    print("Original :", original_text)
    print("Encoded  :", encoded)
    print("Decoded  :", decoded)


    print("\n===== XOR =====")

    xor_key = "CyberKey"

    encoded = xor_encode(
        original_text,
        xor_key
    )

    decoded = xor_decode(
        encoded,
        xor_key
    )

    print("Original :", original_text)
    print("Key      :", xor_key)
    print("Encoded  :", encoded)
    print("Decoded  :", decoded)

    # ==========================================
# MULTI-LAYER ENCODING
# ==========================================

def multi_layer_encode(data):
    """
    Apply multiple harmless text transformations:
    Base64 -> Hex
    """

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    # Layer 1: Base64
    layer1 = base64_encode(data)

    # Layer 2: Hex
    layer2 = hex_encode(layer1)

    return layer2


def multi_layer_decode(data):
    """
    Reverse the multi-layer transformation:
    Hex -> Base64
    """

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    # Reverse Layer 2: Hex
    layer1 = hex_decode(data)

    # Reverse Layer 1: Base64
    original = base64_decode(layer1)

    return original