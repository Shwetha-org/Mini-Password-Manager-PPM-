
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptionManager:
    def __init__(self):
        self.key = None

    def generate_key_from_password(self,password: str, salt: bytes) -> bytes:

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_password(self, plaintext:str) -> str:
        """Encrypt a password using AES-256"""
        if not self.key:
            raise ValueError("Encryption key not set")
        f = Fernet(self.key)
        encrypted = f.encrypt(plaintext.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_password(self, encrypted_text: str) -> str:
        """Decrypt a password using AES-256"""
        if not self.key:
            raise ValueError("Encryption key not set")
        f = Fernet(self.key)
        encrypted = base64.b64decode(encrypted_text.encode())
        decrypted = f.decrypt(encrypted)
        return decrypted.decode()

