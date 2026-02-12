"""Security utilities for password hashing and encryption."""
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from app.config import get_settings

settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain password.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


# Encryption for sensitive user data (API keys, credentials)
_cipher = Fernet(settings.ENCRYPTION_KEY.encode())


def encrypt_value(value: str) -> str:
    """
    Encrypt a sensitive value.

    Args:
        value: Plain text value to encrypt

    Returns:
        Encrypted value as string
    """
    if not value:
        return ""
    return _cipher.encrypt(value.encode()).decode()


def decrypt_value(encrypted_value: str) -> str:
    """
    Decrypt an encrypted value.

    Args:
        encrypted_value: Encrypted value from database

    Returns:
        Decrypted plain text value
    """
    if not encrypted_value:
        return ""
    return _cipher.decrypt(encrypted_value.encode()).decode()
