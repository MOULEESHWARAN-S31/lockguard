
from telegram import send_message
from datetime import datetime


def send_startup_notification():
    startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        "🚀 LAPTOP STARTED!\n\n"
        f"Time: {startup_time}\n"
        "Your Windows system has started successfully.\n\n"
        "LaptopWatch is ready to monitor lock and unlock events."
    )

    success = send_message(message)

    if success:
        print("Startup notification sent successfully!")
    else:
        print("Failed to send startup notification.")

    return success


if __name__ == "__main__":
    send_startup_notification()
