# Mini Password Manager (PPM)
Python-based personal password manager with AES encryption and master key authentication. 

##Features
- AES-256 encyrption for secure password storage
- Master Password Authentication
- Storing and Retrieving usernames & passwords
- Command-Line Interface

##Setup
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

### Notes for Users
- Keep `storage.json` empty initially; the program will populate it with encrypted data automatically.  
- **Important:** Do not commit real passwords to this repository. This project is meant for testing and learning purposes only.  
- `.gitignore` is configured to exclude sensitive files like `storage.json` and the virtual environment folder (`venv/`).  
