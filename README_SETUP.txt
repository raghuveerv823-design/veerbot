═══════════════════════════════════════════════════════════════════════
          VEERBOT - SETUP AUR USAGE INSTRUCTIONS
═══════════════════════════════════════════════════════════════════════

📁 WORKSPACE STRUCTURE:
────────────────────────────────────────────────────────────────────────

VEERBOT/
├── main.exe                    ← C++ Bot Server (compiled)
├── main.cpp                    ← C++ Bot Source Code
├── botfile.txt                 ← Bot Q&A Database
├── unknown_questions.txt       ← Unknown questions log
├── bot_logs.txt                ← Server logs
├── index.html                  ← Web Interface (Open in browser)
└── python_client.py            ← Python Client Script


═══════════════════════════════════════════════════════════════════════
STEP 1: MAIN BOT SERVER START KARNA
═══════════════════════════════════════════════════════════════════════

PowerShell ya Command Prompt kholo aur yeh command run karo:

    cd c:\Users\user\Downloads\veerbot
    main.exe

Ya Default Port (8080) use karte hue koi aur port set karna chahte ho to:

    main.exe --port 9000      (Port 9000 set karega)
    main.exe --external        (External connections allow karega)
    main.exe --verbose         (Debug information show karega)

Example:
    main.exe --port 5000 --verbose --external


═══════════════════════════════════════════════════════════════════════
STEP 2: WEB PAGE SE BOT USE KARNA
═══════════════════════════════════════════════════════════════════════

1. Main.exe running hai ye ensure karo (Step 1 complete hona chahiye)

2. Explorer/Finder kholo aur index.html file dhundo

3. index.html par double-click karo OR
   Right-click → Open with → Your Web Browser

4. Browser mein open ho jayega. Ab apne questions puchh sakte ho!

🌐 Keyboard Shortcut:
   - "Enter" key dbaane se message bhej jaega
   - "exit" likhakar quit kar sakte ho


═══════════════════════════════════════════════════════════════════════
STEP 3: PYTHON SE BOT USE KARNA
═══════════════════════════════════════════════════════════════════════

Prerequisites (First time only):
────────────────────────────────

1. Python installed hai ye check karo:
   python --version

2. Requests library install karo (agar nahi hai to):
   pip install requests

   ya
   
   pip3 install requests


Run Python Client:
────────────────────────────────

1. Main.exe running hai ye ensure karo (Step 1 complete hona chahiye)

2. Naya PowerShell/Command Prompt window kholo:
   cd c:\Users\user\Downloads\veerbot
   python python_client.py

3. Terminal mein questions type karo aur Enter dbaao

4. "exit" likhakar quit karo


Python Code Example (Apna Script Banana Chahte Ho):
────────────────────────────────────────────────────

import requests

def ask_bot(question):
    response = requests.get(
        "http://127.0.0.1:8080/",
        params={'question': question}
    )
    data = response.json()
    print(f"Bot: {data['answer']}")

# Use karna:
ask_bot("College mein admission kaise hota hai?")


═══════════════════════════════════════════════════════════════════════
ADVANCED: MULTIPLE DEVICES SE USE KARNA
═══════════════════════════════════════════════════════════════════════

Agar doosre computer/laptop/phone se bot ko access karna chahte ho:

1. Bot Server ko External Mode mein start karo:
   main.exe --external

2. Aapne Computer ka IP address dhundo:
   Windows PowerShell mein: ipconfig
   IPv4 Address dhundo (usually 192.168.x.x ya 10.x.x.x)

3. Doosre Device se:

   Web Browser:
   - Address bar mein likho: http://YOUR_IP:8080
   - Example: http://192.168.1.5:8080

   Python Client:
   - python_client.py mein line 6 change karo:
     BOT_HOST = "192.168.1.5"  (apne IP se replace karo)

   CURL/Command Line:
   curl "http://192.168.1.5:8080/?question=hello"


═══════════════════════════════════════════════════════════════════════
TROUBLESHOOTING / COMMON ISSUES
═══════════════════════════════════════════════════════════════════════

❌ Issue: "Port already in use" error
   Solution:
   - Koi aur main.exe process running hai
   - taskkill /IM main.exe /F  (kill karo)
   - Ya alag port use karo: main.exe --port 9000

❌ Issue: Web page blank ho raha hai
   Solution:
   - Main.exe running hai ye check karo
   - Status mein "Connected" message dekhna chahiye
   - Refresh page (F5)

❌ Issue: Python client: "ConnectionError"
   Solution:
   - Main.exe running hai ye check karo (command prompt mein)
   - Port number same hona chahiye (8080 by default)
   - Firewall check karo (allow karo)

❌ Issue: "requests module not found"
   Solution:
   - pip install requests
   - ya python -m pip install requests

❌ Issue: botfile.txt not found
   Solution:
   - botfile.txt wali directory mein cd karo
   - Ya main.exe --config /path/to/botfile.txt


═══════════════════════════════════════════════════════════════════════
IMPORTANT: BOTFILE FORMAT
═══════════════════════════════════════════════════════════════════════

botfile.txt format:

keyword1|keyword2|keyword3:Answer to give

Examples:

admission|apply|form:Admission ke liye college website visit karo
fees|fees structure|tuition:Fees structure college office mein hai
library|books|study:Library main building ke 2nd floor par hai

Note:
- Keywords ko | (pipe) se separate karo
- Colon (:) se answer separate karo
- # dbaake comments add kar sakte ho


═══════════════════════════════════════════════════════════════════════
ADMIN PANEL ACCESS (CONSOLE MEIN)
═══════════════════════════════════════════════════════════════════════

Main.exe console mein type karo "admin" aur Enter do:

1. Username: chatbot
2. Password: veer9301

Options:
1. Add new Q&A
2. Update existing Q&A
3. View unknown questions
4. Exit


═══════════════════════════════════════════════════════════════════════
COMPILATION (Agar main.cpp modify kiya ho)
═══════════════════════════════════════════════════════════════════════

PowerShell mein:

g++ -o main.exe main.cpp -lws2_32

Ya Visual Studio Code mein:
- Ctrl+Shift+B


═══════════════════════════════════════════════════════════════════════
SUMMARY / QUICK REFERENCE
═══════════════════════════════════════════════════════════════════════

Step 1 - Start Bot:
   main.exe

Step 2 - Web Browser (New window):
   index.html kholo (double-click)

Step 3 - Python Client (New terminal):
   python python_client.py

That's it! 🎉


═══════════════════════════════════════════════════════════════════════
