import getpass
import json
from encryption import EncryptionManager

class PasswordManager:
    def __init__(self):
        self.storage_file = "storage.json"
        self.master_file = "master.key"
        self.encryption_manager = EncryptionManager()

    def mainMenu(self):
        print("="*40)
        print("    MINI PASSWORD MANAGER")
        print("="*40)
        print("1. Add New Password")
        print("2. Retrieve Password") 
        print("3. View All Services")
        print("4. Exit")
        print("="*40)

    def getUserChoice(self):
        try:
            choice = input("Enter your choice (1-4): ")
            return int(choice)
        except ValueError:
            return -1
        
    def run(self):
        print("Welcome to your Password Manager!")
        print("DEBUG: Program started successfully")  # Add this
        
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
                print("Goodbye! 👋")
                break
            else:
                print("❌ Invalid choice! Please try again.")

    def add_password_flow(self):
        print("Adding New Password!")

        service = input("Enter the service name (ex: Gmail, Netflix etc) : ")
        username = input("Enter username/email: ")
        print("Note: Password will not appear on screen as you type")
        password = getpass.getpass("Enter the password: ")

        self.save_password(service, username, password)

        print(f"\n✅ Added entry for {service}!")
        print(f"   Username: {username}")
        print(f"   Password: {'*' * len(password)}")

    def save_password(self, service, username, password):
        
        # Encrypts the password before saving
        encrypted_password = self.encryption_manager.encrypt_password(password)

        entry = {
            "service": service,
            "username": username,
            "password": encrypted_password
        }

        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError :
            data=[]
        except json.JSONDecodeError:
            # Handle corrupted JSON
            print("⚠️  Storage file corrupted, starting fresh...")
            data = []

        data.append(entry)

        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Saved {service} entry to {self.storage_file}")

    def retrieve_password_flow(self):
        print("Retrieving Password!")

        service = input("Enter the service name to retrieve: ")

        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
        
            found = False
            for entry in data:
                if service.lower() in entry["service"].lower():
                    
                    decrypted_password = self.encryption_manager.decrypt_password(entry['password'])

                    print(f"\n✅ Found {entry['service']}!")
                    print(f"   Username: {entry['username']}")
                    print(f"   Password: {decrypted_password}")
                    found = True

            if not found :
                print(f"\n❌ No entry found for '{service}'")

        except FileNotFoundError:
            print("\n❌ No passwords stored yet!")
        except json.JSONDecodeError:
            print("\n❌ Storage file is corrupted")

    def view_services_flow(self):
        print("Showing all Stored Services!")

        try:
            with open(self.storage_file,'r') as f:
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


if __name__ == "__main__":
    manager = PasswordManager()
    manager.run()
    
