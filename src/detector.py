
import time
import subprocess
import os
import sys

# Import Telegram notification function
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__))
)

from telegram import send_message


# Windows Security Event IDs
LOCK_EVENT_ID = 4800
UNLOCK_EVENT_ID = 4801

POLL_INTERVAL = 2



def run_powershell(command):
    result = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            command
        ],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip()



def get_latest_record():
    """Get the latest Security log record ID."""

    command = (
        "Get-WinEvent -LogName Security -MaxEvents 1 "
        "| ForEach-Object { $_.RecordId }"
    )

    output = run_powershell(command)

    return int(output)


def get_security_events(last_record):
    """Find new lock and unlock events."""

    command = (
        f'$events = Get-WinEvent -LogName Security '
        f'-FilterXPath "*[System[((EventID={LOCK_EVENT_ID}) '
        f'or (EventID={UNLOCK_EVENT_ID})) '
        f'and (EventRecordID > {last_record})]]" '
        f'-ErrorAction SilentlyContinue; '
        f'$events | Sort-Object RecordId | '
        f'ForEach-Object {{ '
        f'"$($_.RecordId)|$($_.Id)|$($_.TimeCreated.ToString(\'yyyy-MM-dd HH:mm:ss\'))" '
        f'}}'
    )

    output = run_powershell(command)

    if not output:
        return []

    events = []

    for line in output.splitlines():
        record_id, event_id, event_time = line.split("|", 2)

        events.append(
            (int(record_id), int(event_id), event_time)
        )

    return events


def monitor():
    """Monitor Windows lock and unlock events."""

    print("================================")
    print("         LAPTOPWATCH")
    print("================================")

    last_record = get_latest_record()

    print("Security log access: SUCCESS")
    print("Starting record:", last_record)
    print("Lock detection: ENABLED")
    print("Unlock detection: ENABLED")
    print("Telegram notifications: ENABLED")
    print("Monitoring Windows events...")
    print("Press CTRL+C to stop.")

    while True:

        try:
            events = get_security_events(last_record)

            for record_id, event_id, event_time in events:

                if record_id <= last_record:
                    continue

                if event_id == LOCK_EVENT_ID:

                    title = "🔒 LAPTOP LOCKED!"
                    message = (
                        "🔒 LAPTOP LOCKED!\n\n"
                        f"Time: {event_time}\n"
                        f"Event ID: {event_id}\n"
                        "LaptopWatch detected a Windows lock."
                    )

                elif event_id == UNLOCK_EVENT_ID:

                    title = "🔓 LAPTOP UNLOCKED!"
                    message = (
                        "🔓 LAPTOP UNLOCKED!\n\n"
                        f"Time: {event_time}\n"
                        f"Event ID: {event_id}\n"
                        "LaptopWatch detected a Windows unlock."
                    )

                else:
                    last_record = record_id
                    continue

                print("\n================================")
                print(title)
                print("Event ID:", event_id)
                print("Record ID:", record_id)
                print("Time:", event_time)

                success = send_message(message)

                if success:
                    print("Telegram alert: SENT")
                else:
                    print("Telegram alert: FAILED")

                print("================================")

                last_record = record_id

        except Exception as error:
            print("Monitoring error:", repr(error))

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":

    try:
        monitor()

    except KeyboardInterrupt:
        print("\nLaptopWatch stopped.")

    except Exception as error:
        print("\nLaptopWatch startup error:", repr(error))
