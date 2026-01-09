import os
import getpass
import json
from encryption import EncryptionManager
from auth import AuthManager


class PasswordManager:
    def __init__(self, encryption_manager, auth_manager):
        self.storage_file = "storage.json"
        self.master_file = "master.key"
        self.encryption_manager = encryption_manager
        self.auth_manager = auth_manager


    def mainMenu(self):
        print("=" * 40)
        print("    MINI PASSWORD MANAGER")
        print("=" * 40)
        print("1. Add New Password")
        print("2. Retrieve Password")
        print("3. View All Services")
        print("4. Update Password")
        print("5. Delete Account")
        print("6. Change Master Password")
        print("7. Exit")
        print("=" * 40)

    def getUserChoice(self):
        try:
            choice = input("Enter your choice (1-7): ")
            return int(choice)
        except ValueError:
            return -1

    def run(self):
        print("Welcome to your Password Manager!")

        while True:
            self.mainMenu()
            choice = self.getUserChoice()

            if choice == 1:
                self.add_password_flow()
            elif choice == 2:
                self.retrieve_password_flow()
            elif choice == 3:
                self.view_services_flow()
            elif choice == 4:
                self.update_password_flow()
            elif choice == 5:
                self.delete_account_flow()
            elif choice == 6:
                self.auth_manager.change_master_password(self.storage_file)
            elif choice == 7:
                print("Goodbye! 👋")
                break
            else:
                print("❌ Invalid choice! Please try again.")

    def add_password_flow(self):
        print("Adding New Password!")

        # Validate service
        while True:
            service = input("Enter the service name (ex: Gmail, Netflix etc): ").strip()
            if service:
                break
            print("Service name cannot be empty.")

        # Validate username
        while True:
            username = input("Enter username/email: ").strip()
            if username:
                break
            print("Username cannot be empty.")

        print("Note: Password will not appear on screen as you type")

        # Validate password
        while True:
            password = getpass.getpass("Enter the password: ")
            if password:
                break
            print("Password cannot be empty.")

        self.save_password(service, username, password)

        print(f"\n✅ Added entry for {service}!")
        print(f"   Username: {username}")
        print(f"   Password: {'*' * len(password)}")

        # Optional: clear plaintext variable
        password = None

    def save_password(self, service, username, password):
        # Encrypts the password before saving
        encrypted_password = self.encryption_manager.encrypt_password(password)
        service_key = service.strip().lower()

        entry = {
            "service": service,
            "service_key": service_key,
            "username": username,
            "password": encrypted_password,
        }

        try:
            with open(self.storage_file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            # Handle corrupted JSON
            print("⚠️  Storage file corrupted, starting fresh...")
            data = []

        data.append(entry)

        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Saved {service} entry to {self.storage_file}")

    def retrieve_password_flow(self):
        print("Retrieving Password!")
        service = input("Enter the service name to retrieve: ").strip()

        if not service:
            print("Service name cannot be empty.")
            return

        try:
            with open(self.storage_file, "r") as f:
                data = json.load(f)

            query = service.strip().lower()
            matches = [
                e for e in data
                if e.get("service_key", e["service"].lower()) == query
            ]

            if not matches:
                print(f"\n❌ No entry found for '{service}'")
                return

            # If only one match, show it directly
            if len(matches) == 1:
                entry = matches[0]
            else:
                # Show all matching accounts and let user choose
                print(f"\nFound {len(matches)} accounts for '{service}':")
                for i, entry in enumerate(matches, 1):
                    print(f" {i}. {entry['service']} - {entry['username']}")

                while True:
                    try:
                        choice = int(input("Select an account (number): "))
                        if 1 <= choice <= len(matches):
                            entry = matches[choice - 1]
                            break
                        else:
                            print("Please enter a valid number.")
                    except ValueError:
                        print("Please enter a valid number.")

            try:
                decrypted_password = self.encryption_manager.decrypt_password(entry["password"])
            except Exception:
                print("\n❌ Failed to decrypt this entry. It may be corrupted.")
                return

            print(f"\n✅ Found {entry['service']}!")
            print(f" Username: {entry['username']}")
            print(f" Password: {decrypted_password}")

        except FileNotFoundError:
            print("\n❌ No passwords stored yet!")
        except json.JSONDecodeError:
            print("\n❌ Storage file is corrupted")

    def view_services_flow(self):
        print("Showing all Stored Services!")

        try:
            with open(self.storage_file, "r") as f:
                data = json.load(f)

            if not data:
                print("No services stored yet!")
                return

            print(f"Found {len(data)} service(s): ")
            for i, entry in enumerate(data, 1):
                print(f"   {i}. {entry['service']} - {entry['username']}")
        except FileNotFoundError:
            print("No passwords stored yet!")
        except json.JSONDecodeError:
            print("Storage file is corrupted")

    def update_password_flow(self):
        print("Update Password")
        data, idx, entry = self._choose_account("update")
        if data is None or entry is None:
            return

        print(f"Updating password for {entry['service']} - {entry['username']}")
        new_password = getpass.getpass("Enter new password: ")
        confirm = getpass.getpass("Confirm new password: ")

        if new_password != confirm:
            print("❌ Passwords do not match. Aborting update.")
            return

        encrypted = self.encryption_manager.encrypt_password(new_password)
        data[idx]["password"] = encrypted

        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=2)

        print("✅ Password updated.")

        # Optional: clear plaintext
        new_password = None
        confirm = None

    def delete_account_flow(self):
        print("Delete Account")
        data, idx, entry = self._choose_account("delete")
        if data is None or entry is None:
            return

        confirm = input(
            f"Are you sure you want to delete {entry['service']} - {entry['username']}? (y/n): "
        ).strip().lower()
        if confirm != "y":
            print("Deletion cancelled.")
            return

        # Remove and save
        del data[idx]
        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=2)

        print("✅ Account deleted.")

    def _load_data(self):
        try:
            with open(self.storage_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("\n❌ No passwords stored yet!")
            return None
        except json.JSONDecodeError:
            print("\n❌ Storage file is corrupted")
            return None

    def _choose_account(self, action_label: str):
        # Ensure non-empty service name
        while True:
            service = input(f"Enter the service name to {action_label}: ").strip()
            if service:
                break
            print("Service name cannot be empty.")
        query = service.lower()

        data = self._load_data()
        if data is None:
            return None, None, None

        matches = [
            (idx, entry)
            for idx, entry in enumerate(data)
            if entry.get("service_key", entry["service"].lower()) == query
        ]

        if not matches:
            print(f"\n❌ No entry found for '{service}'")
            return None, None, None

        if len(matches) == 1:
            idx, entry = matches[0]
            return data, idx, entry

        print(f"\nFound {len(matches)} accounts for '{service}':")
        for i, (_, entry) in enumerate(matches, 1):
            print(f" {i}. {entry['service']} - {entry['username']}")

        while True:
            try:
                choice = int(input("Select an account (number): "))
                if 1 <= choice <= len(matches):
                    idx, entry = matches[choice - 1]
                    return data, idx, entry
                else:
                    print("Please enter a valid number.")
            except ValueError:
                print("Please enter a valid number.")


if __name__ == "__main__":
    encryption_manager = EncryptionManager()
    auth_manager = AuthManager(encryption_manager)

    if not os.path.exists("master.key"):
        auth_manager.setup_master_password()
    else:
        if not auth_manager.verify_master_password():
            exit(1)

    manager = PasswordManager(encryption_manager, auth_manager)
    manager.run()
