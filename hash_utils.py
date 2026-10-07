import hashlib


def calculate_sha256(data):
    """
    Calculate SHA-256 hash of text data.
    """

    if not isinstance(data, str):
        raise ValueError("Input must be text.")

    return hashlib.sha256(
        data.encode("utf-8")
    ).hexdigest()


def compare_hashes(original_data, transformed_data):
    """
    Calculate and return SHA-256 hashes
    for original and transformed data.
    """

    original_hash = calculate_sha256(original_data)
    transformed_hash = calculate_sha256(transformed_data)

    return {
        "original_hash": original_hash,
        "transformed_hash": transformed_hash
    }


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    original_text = "Hello Cyber Security"

    transformed_text = "SGVsbG8gQ3liZXIgU2VjdXJpdHk="

    hashes = compare_hashes(
        original_text,
        transformed_text
    )

    print("\n===== SHA-256 HASH TEST =====")

    print("Original Hash   :", hashes["original_hash"])
    print("Transformed Hash:", hashes["transformed_hash"])