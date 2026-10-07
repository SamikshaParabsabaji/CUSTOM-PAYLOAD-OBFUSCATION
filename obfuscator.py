import base64
import string


# ==========================================
# CUSTOM SUBSTITUTION
# ==========================================

def custom_substitute_encode(data, shift=3):
    """
    Apply a simple reversible character substitution.

    Only printable ASCII characters are transformed.
    """

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    if not isinstance(shift, int):
        raise ValueError("Shift must be an integer.")

    if shift < 0 or shift > 94:
        raise ValueError("Shift must be between 0 and 94.")

    printable = string.printable[:-6]
    result = []

    for char in data:

        if char in printable:
            index = printable.index(char)
            new_index = (index + shift) % len(printable)
            result.append(printable[new_index])

        else:
            result.append(char)

    return "".join(result)


def custom_substitute_decode(data, shift=3):
    """
    Reverse the custom substitution.
    """

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    if not isinstance(shift, int):
        raise ValueError("Shift must be an integer.")

    if shift < 0 or shift > 94:
        raise ValueError("Shift must be between 0 and 94.")

    printable = string.printable[:-6]
    result = []

    for char in data:

        if char in printable:
            index = printable.index(char)
            new_index = (index - shift) % len(printable)
            result.append(printable[new_index])

        else:
            result.append(char)

    return "".join(result)


# ==========================================
# MULTI-LAYER TRANSFORMATION
# ==========================================

def multi_layer_encode(data):
    """
    Apply multiple harmless transformations:

    Layer 1 -> Base64
    Layer 2 -> Custom substitution
    """

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    # Layer 1: Base64
    layer1 = base64.b64encode(
        data.encode("utf-8")
    ).decode("utf-8")

    # Layer 2: Custom substitution
    layer2 = custom_substitute_encode(
        layer1,
        shift=3
    )

    return layer2


def multi_layer_decode(data):
    """
    Reverse the multi-layer transformation.
    """

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    # Reverse Layer 2
    layer1 = custom_substitute_decode(
        data,
        shift=3
    )

    # Reverse Layer 1
    try:
        decoded = base64.b64decode(
            layer1.encode("utf-8"),
            validate=True
        )

        return decoded.decode("utf-8")

    except Exception:
        raise ValueError(
            "Invalid multi-layer encoded data."
        )


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    original_text = "Hello Cyber Security"

    print("\n===== CUSTOM SUBSTITUTION =====")

    encoded = custom_substitute_encode(
        original_text,
        shift=3
    )

    decoded = custom_substitute_decode(
        encoded,
        shift=3
    )

    print("Original :", original_text)
    print("Encoded  :", encoded)
    print("Decoded  :", decoded)


    print("\n===== MULTI-LAYER =====")

    encoded = multi_layer_encode(
        original_text
    )

    decoded = multi_layer_decode(
        encoded
    )

    print("Original :", original_text)
    print("Encoded  :", encoded)
    print("Decoded  :", decoded)