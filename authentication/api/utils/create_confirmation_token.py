import secrets
import hashlib

def create_confirmation_token(length=30):
    # Generate a random string using secrets.token_hex
    random_string = secrets.token_hex(length // 2)  # Each byte is represented by 2 hex characters

    # Hash the random string using hashlib
    hashed_string = hashlib.sha256(random_string.encode()).hexdigest()

    return hashed_string
