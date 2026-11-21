
import sys
import os
import time

# Add src folder to Python path
SRC_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "src"
)

sys.path.insert(0, SRC_FOLDER)

from startup_alert import send_startup_notification
from detector import monitor


def main():
    print("================================")
    print("       LAPTOPWATCH STARTING")
    print("================================")

    # Retry startup notification if network is not ready
    for attempt in range(1, 11):
        print(f"Startup notification attempt: {attempt}/10")

        if send_startup_notification():
            break

        if attempt < 10:
            print("Waiting 15 seconds before retry...")
            time.sleep(15)

    print("\nStarting lock/unlock monitoring...\n")

    monitor()


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nLaptopWatch stopped.")

    except Exception as error:
        print("\nLaptopWatch error:", repr(error))
