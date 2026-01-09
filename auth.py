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

    def _save_master_data(self, salt: bytes, key: bytes):
        # store salt + a hash of the key for verification
        digest = hashes.Hash(hashes.SHA256())
        digest.update(key)
        key_hash = digest.finalize()

        data = {
            "salt": base64.b64encode(salt).decode(),
            "key_hash": base64.b64encode(key_hash).decode(),
        }
        with open(self.master_file, "w") as f:
            json.dump(data, f, indent=2)

    def _load_master_data(self):
        with open(self.master_file, "r") as f:
            data = json.load(f)
        salt = base64.b64decode(data["salt"].encode())
        key_hash = base64.b64decode(data["key_hash"].encode())
        return salt, key_hash

    def setup_master_password(self):
        print("🔐 Set up a master password")
        while True:
            pwd1 = getpass.getpass("Enter a new master password: ")
            pwd2 = getpass.getpass("Confirm master password: ")
            if pwd1 != pwd2:
                print("Passwords do not match, try again.")
            elif not pwd1:
                print("Password cannot be empty.")
            else:
                break

        salt = os.urandom(16)
        key = self.encryption_manager.generate_key_from_password(pwd1, salt)
        self._save_master_data(salt, key)
        self.encryption_manager.key = key
        print("✅ Master password set successfully.")

    def verify_master_password(self):
        print("🔐 Master password required")
        try:
            salt, stored_key_hash = self._load_master_data()
        except FileNotFoundError:
            print("No master password file found.")
            return False

        for _ in range(3):
            pwd = getpass.getpass("Enter master password: ")
            key = self.encryption_manager.generate_key_from_password(pwd, salt)

            digest = hashes.Hash(hashes.SHA256())
            digest.update(key)
            key_hash = digest.finalize()

            if key_hash == stored_key_hash:
                self.encryption_manager.key = key
                print("✅ Authentication successful.")
                return True
            else:
                print("❌ Incorrect master password.")

        print("Too many failed attempts. Exiting.")
        return False

    def change_master_password(self, storage_file: str):
        print("🔐 Change master password")

        # 1) Verify current master password
        if not self.verify_master_password():
            return False

        # 2) Load and decrypt existing passwords with the old key
        try:
            with open(storage_file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            print("❌ Storage file is corrupted; cannot safely re-encrypt.")
            return False

        decrypted_entries = []
        for entry in data:
            try:
                plaintext = self.encryption_manager.decrypt_password(entry["password"])
            except Exception:
                print("❌ Failed to decrypt an entry; aborting change.")
                return False
            decrypted_entries.append(
                {
                    "service": entry["service"],
                    "service_key": entry.get("service_key", entry["service"].lower()),
                    "username": entry["username"],
                    "password_plain": plaintext,
                }
            )

        # 3) Ask for new master password
        while True:
            new_pwd1 = getpass.getpass("Enter new master password: ")
            new_pwd2 = getpass.getpass("Confirm new master password: ")
            if new_pwd1 != new_pwd2:
                print("Passwords do not match, try again.")
            elif not new_pwd1:
                print("Password cannot be empty.")
            else:
                break

        # 4) Derive new key and save new master file
        new_salt = os.urandom(16)
        new_key = self.encryption_manager.generate_key_from_password(new_pwd1, new_salt)
        self._save_master_data(new_salt, new_key)
        self.encryption_manager.key = new_key

        # 5) Re-encrypt all entries with the new key
        reencrypted_data = []
        for entry in decrypted_entries:
            encrypted = self.encryption_manager.encrypt_password(entry["password_plain"])
            reencrypted_data.append(
                {
                    "service": entry["service"],
                    "service_key": entry["service_key"],
                    "username": entry["username"],
                    "password": encrypted,
                }
            )

        with open(storage_file, "w") as f:
            json.dump(reencrypted_data, f, indent=2)

        print("✅ Master password changed and all data re-encrypted.")
        return True
