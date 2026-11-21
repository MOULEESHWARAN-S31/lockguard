
# 💻 LaptopWatch

> A lightweight Windows desktop monitoring application that sends real-time Telegram notifications when important laptop events occur — silently running in the background, always keeping you informed.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-0078D6?logo=windows&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-26A5E4?logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [How It Works](#-how-it-works)
4. [Technologies Used](#-technologies-used)
5. [Project Folder Structure](#-project-folder-structure)
6. [Prerequisites](#-prerequisites)
7. [Installation and Setup](#-installation-and-setup)
8. [Telegram Bot Configuration](#-telegram-bot-configuration)
9. [Environment Variable Configuration](#-environment-variable-configuration)
10. [How to Run the Project](#-how-to-run-the-project)
11. [Windows Task Scheduler Configuration](#-windows-task-scheduler-configuration)
12. [How Lock and Unlock Detection Works](#-how-lock-and-unlock-detection-works)
13. [Sample Telegram Notifications](#-sample-telegram-notifications)
14. [Troubleshooting](#-troubleshooting)
15. [Security and Privacy](#-security-and-privacy)
16. [Future Enhancements](#-future-enhancements)
17. [Author and Acknowledgements](#-author-and-acknowledgements)

---

## 🔍 Project Overview

**LaptopWatch** is a Python-based Windows desktop monitoring tool designed to keep you informed about key laptop activity — no matter where you are. It runs silently in the background using `pythonw.exe` (which suppresses the terminal window) and communicates with you via a **Telegram bot**.

Whether you want to know when someone has logged into your laptop, locked it, or unlocked it, LaptopWatch delivers instant, private Telegram notifications directly to your phone or desktop.

> ⚠️ **Platform Notice:** LaptopWatch is currently designed and tested exclusively for **Windows 11**. It is not compatible with macOS or Linux at this time.

> ℹ️ **Important Distinction:** LaptopWatch detects **Windows user login/logoff sessions** — not physical laptop power-on or shutdown. The startup notification fires when a user **logs into Windows**, not necessarily when the machine boots from a powered-off state.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🟢 **Startup Notification** | Sends a Telegram alert when the user logs into Windows |
| 🔒 **Lock Detection** | Detects when the Windows session is locked (Event ID `4800`) |
| 🔓 **Unlock Detection** | Detects when the Windows session is unlocked (Event ID `4801`) |
| 📬 **Telegram Integration** | All notifications delivered through your personal Telegram bot |
| 🤫 **Silent Background Mode** | Runs with `pythonw.exe` — no visible terminal window |
| ⏰ **Automatic Startup** | Launches automatically via Windows Task Scheduler on user login |

---

## ⚙️ How It Works

Here is the step-by-step workflow of LaptopWatch:

```
User Logs into Windows
        │
        ▼
Task Scheduler triggers main.py (via pythonw.exe)
        │
        ├──► startup_alert.py sends "Login detected" Telegram message
        │
        └──► detector.py starts a continuous monitoring loop
                    │
                    ▼
        Polls Windows Security Event Log
        for Event IDs 4800 and 4801
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
    Event ID 4800        Event ID 4801
    (Lock detected)      (Unlock detected)
          │                   │
          ▼                   ▼
  Sends "🔒 Locked"   Sends "🔓 Unlocked"
  Telegram message     Telegram message
```

### Step-by-Step Breakdown

1. **User logs into Windows** — Windows creates a new user session.
2. **Task Scheduler fires** — A pre-configured task runs `pythonw.exe main.py` silently in the background.
3. **Startup alert is sent** — `startup_alert.py` immediately calls the Telegram Bot API to notify you of the login.
4. **Monitoring begins** — `detector.py` starts polling the **Windows Security Event Log** in a continuous loop.
5. **Lock event detected** — When you lock your screen (Win + L), Windows logs **Event ID 4800**. `detector.py` picks this up and sends a 🔒 lock notification.
6. **Unlock event detected** — When you unlock your screen, Windows logs **Event ID 4801**. `detector.py` sends a 🔓 unlock notification.
7. **Notifications arrive** — All messages are delivered to your Telegram account in real time via the bot.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3** | Core programming language |
| **Windows 11** | Target operating system |
| **Telegram Bot API** | Sending real-time notifications |
| **PowerShell** | Running commands and scripts on Windows |
| **Windows Security Event Logs** | Source of lock/unlock event data |
| **Windows Task Scheduler** | Automatically launching the app on user login |
| `requests` | Making HTTP calls to the Telegram Bot API |
| `python-dotenv` | Loading sensitive credentials from a `.env` file |

---

## 📁 Project Folder Structure

```text
LaptopWatch/
│
├── src/
│   ├── telegram.py        # Handles sending messages via Telegram Bot API
│   ├── detector.py        # Monitors Windows Event Log for lock/unlock events
│   └── startup_alert.py   # Sends a notification when the user logs into Windows
│
├── main.py                # Entry point — orchestrates startup alert and monitoring
├── .env                   # Stores your Telegram bot token and chat ID (NOT uploaded to GitHub)
├── .gitignore             # Tells Git which files to ignore (e.g., .env)
├── requirements.txt       # Python package dependencies
└── README.md              # Project documentation (this file)
```

### File Descriptions

- **`src/telegram.py`** — Contains the function that calls the Telegram Bot API to send a message. All other modules import and use this function.
- **`src/detector.py`** — The core monitoring engine. Continuously queries the Windows Security Event Log, detects Event ID `4800` (lock) and `4801` (unlock), and triggers Telegram notifications.
- **`src/startup_alert.py`** — Runs once at startup. Sends a "user logged in" alert to Telegram immediately when the application starts.
- **`main.py`** — The main entry point. Calls `startup_alert.py` first, then launches the monitoring loop from `detector.py`.
- **`.env`** — A private configuration file holding your `BOT_TOKEN` and `CHAT_ID`. **Never commit this file to GitHub.**
- **`.gitignore`** — Ensures sensitive and unnecessary files (like `.env`) are excluded from version control.
- **`requirements.txt`** — Lists all Python libraries needed to run the project.

---

## 📋 Prerequisites

Before setting up LaptopWatch, make sure you have the following:

- ✅ **Windows 11** (Windows 10 may also work but is not officially tested)
- ✅ **Python 3.8 or higher** installed — [Download Python](https://www.python.org/downloads/)
- ✅ **pip** (comes bundled with Python)
- ✅ **A Telegram account** — [Download Telegram](https://telegram.org/)
- ✅ **Administrator privileges** on your Windows machine (required for reading Security Event Logs)
- ✅ **Windows Security Auditing enabled** for lock/unlock detection (see [How Lock and Unlock Detection Works](#-how-lock-and-unlock-detection-works))

### Verify Python Installation

Open **PowerShell** and run:

```powershell
python --version
pip --version
```

You should see output like:

```
Python 3.11.5
pip 23.2.1 from ...
```

---

## 🚀 Installation and Setup

Follow these steps carefully to get LaptopWatch running on your machine.

### Step 1 — Clone the Repository

Open **PowerShell** and run:

```powershell
git clone https://github.com/MOULEESHWARAN-S31/lockguard.git
cd lockguard
```

> Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 2 — Create a Virtual Environment (Recommended)

Using a virtual environment keeps your project dependencies isolated from other Python projects.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

You should now see `(venv)` at the beginning of your PowerShell prompt.

> ℹ️ If you get a script execution error, run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Step 3 — Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- `requests` — for making HTTP calls to the Telegram API
- `python-dotenv` — for loading your credentials from the `.env` file

### Step 4 — Create the `.env` File

In the project root directory, create a file named `.env`:

```powershell
New-Item -Name ".env" -ItemType File
```

Then open it in Notepad and add your credentials (see [Environment Variable Configuration](#-environment-variable-configuration)).

---

## 🤖 Telegram Bot Configuration

You need to create a Telegram bot to send notifications. Follow these steps:

### Step 1 — Create a Bot with BotFather

1. Open Telegram and search for **`@BotFather`**.
2. Start a chat and send the command:
   ```
   /newbot
   ```
3. Follow the prompts:
   - Enter a **name** for your bot (e.g., `My LaptopWatch Bot`)
   - Enter a **username** for your bot — must end in `bot` (e.g., `mylaptopwatch_bot`)
4. BotFather will reply with your **bot token**, which looks like:
   ```
   1234567890:ABCDefghIJKlmnoPQRstuvWXyz1234567890
   ```
   > ⚠️ **Keep this token secret!** Anyone with this token can control your bot.

### Step 2 — Get Your Telegram Chat ID

1. Search for your newly created bot in Telegram and start a chat with it (send any message).
2. Open your browser and visit the following URL (replace `YOUR_BOT_TOKEN` with your actual token):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
3. Look for the `"chat"` object in the JSON response:
   ```json
   "chat": {
       "id": 123456789,
       ...
   }
   ```
4. The value of `"id"` is your **Chat ID**.

> ℹ️ If the response is empty (`"result":[]`), make sure you have sent at least one message to your bot first.

---

## 🔐 Environment Variable Configuration

LaptopWatch stores sensitive credentials in a `.env` file to keep them out of your source code and version control.

### `.env` File Format

Open the `.env` file you created earlier and add the following:

```env
BOT_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_telegram_chat_id_here
```

### Example

```env
BOT_TOKEN=1234567890:ABCDefghIJKlmnoPQRstuvWXyz1234567890
CHAT_ID=123456789
```

> ⚠️ **Never upload your `.env` file to GitHub!**
>
> Your `BOT_TOKEN` is essentially a password that grants full control over your Telegram bot. If someone gets this token, they can send messages through your bot, intercept responses, and potentially misuse it. Your `.gitignore` file is already configured to exclude `.env` from version control — never remove it from `.gitignore`.

### Why Use `.env` Instead of Hardcoding?

| Approach | Risk |
|---|---|
| Hardcoding credentials in `.py` files | Anyone who views your code (GitHub, colleagues) can steal your credentials |
| Using `.env` with `.gitignore` | Credentials stay on your local machine only; source code is safe to share |

---

## ▶️ How to Run the Project

### Manual Run (For Testing)

To test LaptopWatch manually, open **PowerShell** in the project directory with **Administrator privileges** and run:

```powershell
python main.py
```

> ℹ️ Running with `python` (not `pythonw`) will show a terminal window — useful for debugging.

You should immediately receive a Telegram message confirming the application started. Lock your screen (Win + L) and unlock it — you should receive corresponding notifications.

### Silent Run (No Terminal Window)

Once everything is working, use `pythonw.exe` to run without a visible terminal:

```powershell
pythonw main.py
```

> ℹ️ To stop a `pythonw` process, open **Task Manager** → find `pythonw.exe` → End Task.

---

## 🗓️ Windows Task Scheduler Configuration

Task Scheduler allows LaptopWatch to start automatically every time you log into Windows — without you needing to do anything manually.

### Method 1 — Using Task Scheduler GUI

1. Press **Win + S** and search for **"Task Scheduler"**, then open it.
2. In the right panel, click **"Create Task"** (not "Create Basic Task" — we need more options).
3. Fill in the **General** tab:
   - **Name:** `LaptopWatch`
   - **Description:** `Monitors laptop lock/unlock events and sends Telegram notifications`
   - ✅ Check **"Run with highest privileges"** (required for reading Security Event Logs)
   - **Configure for:** `Windows 10` (compatible with Windows 11)
4. Go to the **Triggers** tab → Click **"New..."**:
   - **Begin the task:** `At log on`
   - **Specific user:** Select your Windows username
   - Click **OK**
5. Go to the **Actions** tab → Click **"New..."**:
   - **Action:** `Start a program`
   - **Program/script:** Full path to `pythonw.exe`, for example:
     ```
     C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\pythonw.exe
     ```
   - **Add arguments:** `main.py`
   - **Start in:** Full path to your LaptopWatch project folder, for example:
     ```
     D:\LaptopWatch
     ```
   - Click **OK**
6. Go to the **Conditions** tab:
   - ✅ Uncheck **"Start the task only if the computer is on AC power"** (so it also runs on battery)
7. Click **OK** to save the task.

### Finding Your `pythonw.exe` Path

Run this in PowerShell to find the path:

```powershell
(Get-Command pythonw).Source
```

### Method 2 — Using PowerShell (Advanced)

```powershell
$Action = New-ScheduledTaskAction `
    -Execute "C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\pythonw.exe" `
    -Argument "main.py" `
    -WorkingDirectory "D:\LaptopWatch"

$Trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERNAME"

$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask `
    -TaskName "LaptopWatch" `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -RunLevel Highest `
    -Force
```

> Replace the paths with your actual `pythonw.exe` and project paths.

### Verifying the Task

After creating the task, verify it exists:

```powershell
Get-ScheduledTask -TaskName "LaptopWatch"
```

To manually trigger it for testing:

```powershell
Start-ScheduledTask -TaskName "LaptopWatch"
```

---

## 🔐 How Lock and Unlock Detection Works

### Windows Security Event Log

Windows records every significant security-related action in the **Security Event Log**. When you lock or unlock your screen, Windows writes a specific event:

| Event ID | Action | Description |
|---|---|---|
| `4800` | **Workstation Locked** | The Windows session was locked |
| `4801` | **Workstation Unlocked** | The Windows session was unlocked |

LaptopWatch's `detector.py` continuously queries these events using Python's `subprocess` module or the `pywin32` library to call Windows APIs.

### Enabling Security Auditing (Required)

By default, Windows may not log Event IDs `4800` and `4801`. You must enable **"Other Logon/Logoff Events"** auditing.

#### Option A — Using Local Security Policy (GUI)

1. Press **Win + R**, type `secpol.msc`, and press **Enter**.
2. Navigate to:
   ```
   Security Settings
   └── Advanced Audit Policy Configuration
       └── System Audit Policies - Local Group Policy Object
           └── Logon/Logoff
               └── Audit Other Logon/Logoff Events
   ```
3. Double-click **"Audit Other Logon/Logoff Events"**.
4. Check both ✅ **Success** and ✅ **Failure**.
5. Click **OK** and close the window.

#### Option B — Using PowerShell (Run as Administrator)

```powershell
auditpol /set /subcategory:"Other Logon/Logoff Events" /success:enable /failure:enable
```

Verify the setting was applied:

```powershell
auditpol /get /subcategory:"Other Logon/Logoff Events"
```

You should see:

```
Other Logon/Logoff Events    Success and Failure
```

### Why Administrator Privileges Are Required

The **Windows Security Event Log** is a protected system resource. Reading it requires elevated (Administrator) privileges. This is why:
- Task Scheduler must be configured with **"Run with highest privileges"** checked.
- If you run `main.py` manually for testing, you must open PowerShell **as Administrator**.

---

## 📱 Sample Telegram Notifications

Here are examples of what you will receive in Telegram:

### Login / Startup Notification

```
🟢 LaptopWatch Alert

✅ User logged into Windows
🖥️  Computer: DESKTOP-ABC123
👤 User: YourUsername
🕐 Time: 2026-11-21 16:47:27
```

### Lock Notification

```
🔒 LaptopWatch Alert

🔐 Laptop screen has been locked
🖥️  Computer: DESKTOP-ABC123
👤 User: YourUsername
🕐 Time: 2026-11-21 17:05:12
```

### Unlock Notification

```
🔓 LaptopWatch Alert

🔑 Laptop screen has been unlocked
🖥️  Computer: DESKTOP-ABC123
👤 User: YourUsername
🕐 Time: 2026-11-21 17:08:45
```

---

## 🔧 Troubleshooting

### ❌ "No module named 'dotenv'"

**Cause:** `python-dotenv` is not installed.

**Fix:**
```powershell
pip install python-dotenv
```

---

### ❌ "No module named 'requests'"

**Cause:** `requests` is not installed.

**Fix:**
```powershell
pip install requests
```

---

### ❌ Telegram bot is not sending messages

**Possible Causes and Fixes:**

1. **Wrong BOT_TOKEN or CHAT_ID** — Double-check your `.env` file. Make sure there are no extra spaces or quotes.
2. **Bot not started** — Open Telegram, find your bot, and send it `/start`.
3. **No internet connection** — Ensure your machine has internet access.
4. **Firewall blocking outbound HTTPS** — Check that `api.telegram.org` (port 443) is not blocked.

Test your bot manually in PowerShell:

```powershell
$token = "YOUR_BOT_TOKEN"
$chat_id = "YOUR_CHAT_ID"
$message = "Test from PowerShell"
Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/sendMessage" `
    -Method POST `
    -Body @{ chat_id = $chat_id; text = $message }
```

---

### ❌ Lock/Unlock events are not being detected

**Cause:** Windows Security Auditing is not enabled for lock/unlock events.

**Fix:** Follow the steps in [Enabling Security Auditing](#enabling-security-auditing-required).

**Verify events exist in the log:**

```powershell
Get-WinEvent -LogName Security -MaxEvents 20 | Where-Object { $_.Id -in 4800, 4801 } | Select-Object TimeCreated, Id, Message
```

If no results appear after locking and unlocking your screen, auditing is not enabled.

---

### ❌ Task Scheduler not running LaptopWatch

**Checklist:**
- ✅ **"Run with highest privileges"** is checked in Task Scheduler
- ✅ The `pythonw.exe` path is correct (verify with `(Get-Command pythonw).Source`)
- ✅ The **"Start in"** (working directory) path points to the LaptopWatch folder
- ✅ The trigger is set to **"At log on"** for your specific user
- ✅ **"Start the task only if on AC power"** is unchecked (Conditions tab)

Check the Task Scheduler history:

1. Open Task Scheduler → Find your `LaptopWatch` task
2. Click the **"History"** tab at the bottom
3. Look for error codes or failure messages

---

### ❌ "Access is denied" when reading Event Logs

**Cause:** The script is not running with Administrator privileges.

**Fix:** 
- If running manually: open PowerShell **as Administrator** before running `python main.py`
- If using Task Scheduler: ensure **"Run with highest privileges"** is checked

---

### ❌ Multiple instances of LaptopWatch running

**Cause:** Task Scheduler triggered LaptopWatch multiple times (e.g., after multiple logins).

**Fix:** Add a check in `main.py` to exit if another instance is already running, or configure the Task Scheduler task with:
- **If the task is already running:** `Do not start a new instance`

This option is found in the Task Scheduler task's **Settings** tab.

---

## 🔐 Security and Privacy

LaptopWatch is designed with privacy in mind, but please be aware of the following:

| Topic | Details |
|---|---|
| **Credential Storage** | Your `BOT_TOKEN` and `CHAT_ID` are stored only in the local `.env` file and never hardcoded in source files |
| **`.env` and GitHub** | The `.gitignore` file excludes `.env` — **never remove this rule** before pushing to GitHub |
| **Data Sent to Telegram** | Only event-type (locked/unlocked/login), timestamp, computer name, and username are sent — no passwords, files, or sensitive data |
| **Telegram Bot Security** | Only your personal `CHAT_ID` receives notifications; messages cannot be intercepted by other Telegram users |
| **Local-only Monitoring** | LaptopWatch does not connect to any server other than `api.telegram.org` |
| **No Keylogging** | LaptopWatch does **not** log keystrokes, screen content, or any other user activity |
| **Event Log Access** | Requires Administrator privileges — this is a Windows security boundary, not a vulnerability |

> ⚠️ **If you suspect your `BOT_TOKEN` has been exposed** (e.g., accidentally committed to GitHub), immediately go to `@BotFather` on Telegram and issue `/revoke` to generate a new token.

---

## 🚀 Future Enhancements

The following features are planned or under consideration for future versions:

- [ ] **Scheduled Status Reports** — Daily or weekly summaries of lock/unlock activity
- [ ] **Multi-User Support** — Monitor multiple Windows user accounts on the same machine
- [ ] **Offline Queue** — Buffer notifications when internet is unavailable and send them once reconnected
- [ ] **Config File** — Replace `.env` with a `config.json` or TOML file for richer configuration options
- [ ] **System Tray Icon** — Add a visible system tray icon with options to pause/resume monitoring
- [ ] **Activity Log File** — Save all events locally to a `.log` file for historical review
- [ ] **Remote Commands** — Allow sending Telegram commands to the bot to query status or pause monitoring
- [ ] **Failed Login Alerts** — Detect failed Windows login attempts using Event ID `4625`
- [ ] **Custom Message Templates** — Let users customize the notification message format

---

## 👤 Author and Acknowledgements

### Author

**MOULEESHWARAN S**
- GitHub: [@MOULEESHWARAN-S31](https://github.com/MOULEESHWARAN-S31)
- Project Repo: [lockguard](https://github.com/MOULEESHWARAN-S31/lockguard)

### Acknowledgements

- [**Telegram Bot API**](https://core.telegram.org/bots/api) — For providing a simple, reliable messaging platform
- [**python-dotenv**](https://pypi.org/project/python-dotenv/) — For clean and safe environment variable management
- [**Microsoft Docs — Windows Security Event IDs**](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4800) — Official reference for Event ID `4800` and `4801`
- [**Windows Task Scheduler Documentation**](https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page) — For background automation on Windows

---

## 📄 License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute this project for personal or commercial purposes. See the `LICENSE` file for details.

---

<div align="center">

Made with ❤️ and Python · Running silently, watching always 👁️

</div>
=======
# lockguard
A lightweight Python app that monitors Windows Security Event Logs and delivers real-time Telegram notifications for login, lock, and unlock events.
>>>>>>> a61c45daf41db9036a62cff70424164504953a01
