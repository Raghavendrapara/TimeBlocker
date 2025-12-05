TimeBlocker 🕒

TimeBlocker is a lightweight, local Windows desktop application for managing daily time blocks. It sits quietly on your desktop and triggers native Windows notifications when a scheduled time block arrives.

Features

Add/Remove Blocks: Simple input for time (24h format) and description.

Persistence: Auto-saves your schedule to a local JSON file.

Native Notifications: Uses Windows Toast notifications so you don't miss a block even if the app is minimized.

Modern UI: Built with CustomTkinter for a clean, dark-mode look.

Installation

Prerequisites

Python 3.8+ installed on your machine.

Steps

Clone the repository:

git clone [https://github.com/yourusername/timeblocker.git](https://github.com/yourusername/timeblocker.git)
cd timeblocker


Install dependencies:

pip install -r requirements.txt


Run the application:

python main.py


Creating a Standalone Windows Exe

If you want to run this without opening a terminal or installing Python on other machines, you can compile it using pyinstaller.

Install PyInstaller:

pip install pyinstaller


Build the executable:

pyinstaller --noconsole --onefile --name="TimeBlocker" main.py


--noconsole: Hides the black terminal window.

--onefile: Bundles everything into a single .exe file.

Locate your app in the dist/ folder. You can now pin this to your Start Menu or Taskbar.

Data Storage

Your schedule is saved in schedule_data.json located in the same directory as the executable/script.