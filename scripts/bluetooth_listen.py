import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import time

import serial

from utils import Files, SerialConfig, SerialMessage, SerialParser

bluetooth = None


def clear_files() -> None:
    with open(Files.BINARY_FILE, "wb"), open(Files.TEXT_FILE, "w"), open(
        Files.TIMESTAMP_FILE, "w"
    ):
        pass


def on_frame(message: SerialMessage) -> None:
    out_str = f"Received message: {message.message.name}, Payload: {message.payload}, Frame: {message.frame}\n"

    with open(Files.TEXT_FILE, "a") as f:
        f.write(out_str)
        f.flush()

    print(out_str, end="", flush=True)


def on_log(log: str) -> None:
    with open(Files.TEXT_FILE, "a") as f:
        f.write(f"LOG: {log}\n")
        f.flush()

    print(f"LOG: {log}")


def process_bluetooth_data(bluetooth: serial.Serial) -> None:
    parser = SerialParser(on_frame, on_log)

    while True:
        if bluetooth.in_waiting <= 0:
            continue

        data = bluetooth.read(bluetooth.in_waiting)

        for byte in data:
            parser.feed_byte(byte)


def send_data(bluetooth: serial.Serial, message: SerialMessage) -> None:
    print(
        f"Sending message: {message.message.name}, Payload: {message.payload}, Frame: {message.frame}",
        flush=True,
    )
    bluetooth.write(message.frame)


def main() -> None:
    clear_files()

    print(f"Connecting to {SerialConfig.PORT} at {SerialConfig.BAUD_RATE} baud...")
    bluetooth = serial.Serial(
        SerialConfig.PORT, SerialConfig.BAUD_RATE, timeout=SerialConfig.TIMEOUT
    )
    time.sleep(2)  # Wait for the connection to initialize

    print(f"Connected. Listening for data... Saving to {Files.BINARY_FILE}")
    try:
        process_bluetooth_data(bluetooth)

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if "bluetooth" in locals() and bluetooth.is_open:
            bluetooth.close()
            print("Bluetooth connection closed.")


if __name__ == "__main__":
    main()
