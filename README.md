# Mini Password Manager (PPM)

Python-based personal password manager with master password protection and encrypted credential storage using the `cryptography` library.


## Features
- Master password authentication with PBKDF2-derived encryption keys (SHA-256,100k iterations).
- Encrypted password storage using the `cryptography` library's Fernet symmetric encryption (AES + HMAC).
- Add, retrieve, update, and delete stored usernames & passwords.
- Support for multiple accounts per service with an interactive selection in the CLI.
- Command-line interface to list all stored services and associated usernames.
- Change master password command that safely re-encrypts all existing entries with the new key.

## Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/Shwetha-org/Mini-Password-Manager-PPM-.git
   cd Mini-Password-Manager-PPM-

2. **Create a Virtual Environment**

   macOS / Linux : 
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
   Windows :
   ```bash
   python -m venv venv
   venv\Scripts\activate  

3. **Install Dependencies**
   ```bash
   pip install cryptography

4. **Run the Project**
   ```bash
   python main.py
   ```
   Follow the prompts to:
   - Set up or log in with a master password.
   - Add new accounts and passwords.
   - Retrieve, update, or delete stored passwords.
   - Change the master password.

### Notes for Users
- Keep `storage.json` empty initially; the program will populate it with encrypted data automatically.  
- **Important:** Do not commit real passwords to this repository. This project is meant for testing and learning purposes only.  
- `.gitignore` is configured to exclude sensitive files like `storage.json` and the virtual environment folder (`venv/`).  

##License
This project is licensed under the MIT License.
See the `LICENSE` file for details.
