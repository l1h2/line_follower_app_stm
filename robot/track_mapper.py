import atexit
import csv
from io import BufferedWriter, TextIOWrapper
from threading import Lock
from time import monotonic

from utils import Files, OperationData, SerialConfig, clear_operation_logs


class Mapper:
    """
    ### Mapper Class

    Handles the mapping of operation data received from the robot. The log files stay open while
    operation data is received, and buffered data is written to them at least every
    `SerialConfig.LOG_FLUSH_INTERVAL` seconds while it keeps arriving. All methods are thread-safe.

    #### Methods:
    - `handle_operation_data(payload: bytes) -> None`: Handles operation data payload from the robot.
    - `flush() -> None`: Writes the buffered operation data to the log files.
    - `close() -> None`: Writes the buffered operation data and closes the log files.
    - `reset() -> None`: Clears the log files, discarding any buffered operation data.
    """

    def __init__(self) -> None:
        self._operation_data = OperationData()
        self._last_encoder_pose: tuple[int, int, float] = (0, 0, 0)
        self._lock = Lock()
        self._binary_file: BufferedWriter | None = None
        self._csv_files: dict[str, TextIOWrapper] = {}
        self._last_flush_time = monotonic()

        atexit.register(self.close)

    def handle_operation_data(self, payload: bytes) -> None:
        """
        Handles operation data payload from the robot.

        Args:
            payload (bytes): The payload containing operation data.
        """
        with self._lock:
            self._write_binary(payload)

            self._operation_data.update(payload)
            self._write_csv(Files.SENSOR_DATA)
            self._handle_encoder_update()

            if monotonic() - self._last_flush_time >= SerialConfig.LOG_FLUSH_INTERVAL:
                self._flush()

    def flush(self) -> None:
        """
        Writes the buffered operation data to the log files.
        """
        with self._lock:
            self._flush()

    def close(self) -> None:
        """
        Writes the buffered operation data and closes the log files. They are opened again
        when new operation data is received.
        """
        with self._lock:
            self._close()

    def reset(self) -> None:
        """
        Clears the log files, discarding any buffered operation data.
        """
        with self._lock:
            self._close()
            clear_operation_logs()

    def _handle_encoder_update(self) -> None:
        """Updates encoder file if there is a change in position or heading."""
        pose = (
            self._operation_data.x,
            self._operation_data.y,
            self._operation_data.heading,
        )
        if pose == self._last_encoder_pose:
            return

        self._last_encoder_pose = pose
        self._write_csv(Files.ENCODER_DATA)

    def _write_binary(self, payload: bytes) -> None:
        """Writes the raw payload to the binary file."""
        if self._binary_file is None:
            self._binary_file = open(Files.BINARY_FILE, "ab")

        self._binary_file.write(payload)

    def _write_csv(self, filename: str) -> None:
        """Writes the operation data to a CSV file."""
        file = self._csv_files.get(filename)
        if file is None:
            file = open(filename, "a", newline="")
            self._csv_files[filename] = file

        writer = csv.writer(file)
        writer.writerow(
            [
                *self._operation_data.sensors,
                self._operation_data.x,
                self._operation_data.y,
                self._operation_data.heading,
            ]
        )

    def _flush(self) -> None:
        """Writes the buffered data of the open log files."""
        if self._binary_file is not None:
            self._binary_file.flush()
        for file in self._csv_files.values():
            file.flush()

        self._last_flush_time = monotonic()

    def _close(self) -> None:
        """Closes the open log files, writing their buffered data."""
        if self._binary_file is not None:
            self._binary_file.close()
            self._binary_file = None

        for file in self._csv_files.values():
            file.close()
        self._csv_files.clear()
