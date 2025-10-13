import csv

from utils import Files, OperationData


class Mapper:
    """
    ### Mapper Class

    Handles the mapping of operation data received from the robot.

    #### Methods:
    - `handle_operation_data(payload: bytes) -> None`: Handles operation data payload from the robot.
    """

    def __init__(self) -> None:
        self._operation_data = OperationData()
        self._last_encoder_update = OperationData()

    def handle_operation_data(self, payload: bytes) -> None:
        """
        Handles operation data payload from the robot.

        Args:
            payload (bytes): The payload containing operation data.
        """
        with open(Files.BINARY_FILE, "ab") as f:
            f.write(payload)

        self._operation_data.update(payload)
        self._write_csv(Files.SENSOR_DATA)
        self._handle_encoder_update(payload)

    def _handle_encoder_update(self, payload: bytes) -> None:
        """Updates encoder file if there is a change in position or heading."""
        if (
            self._operation_data.x == self._last_encoder_update.x
            and self._operation_data.y == self._last_encoder_update.y
            and self._operation_data.heading == self._last_encoder_update.heading
        ):
            return

        self._last_encoder_update.update(payload)
        self._write_csv(Files.ENCODER_DATA)

    def _write_csv(self, filename: str) -> None:
        """Writes the operation data to a CSV file."""
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    *self._operation_data.sensors,
                    self._operation_data.x,
                    self._operation_data.y,
                    self._operation_data.heading,
                ]
            )
