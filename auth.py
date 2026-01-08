
import json
import getpass
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AuthManager:
    def __init__(self, encryption_manager):
        self.master_file = "master.key"
        self.encryption_manager = encryption_manager

    