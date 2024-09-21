import bcrypt

def get_password_hash(password: str) -> str:
    """Hashes the password using bcrypt."""
    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # Return the hashed password as a UTF-8 encoded string
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against the stored hashed password."""
    # Convert to byte format
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')

    # Print debug information
    print(f"Plain Password (str): {plain_password}")
    print(f"Plain Password (bytes): {plain_password_bytes}")
    print(f"Hashed Password (str): {hashed_password}")
    print(f"Hashed Password (bytes): {hashed_password_bytes}")
    print(f"Length of Plain Password (bytes): {len(plain_password_bytes)}")
    print(f"Length of Hashed Password (bytes): {len(hashed_password_bytes)}")

    # Perform verification
    verification = bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    print(f"Verification Result: {verification}")
    return verification