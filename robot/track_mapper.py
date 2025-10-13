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

    def handle_operation_data(self, payload: bytes) -> None:
        """
        Handles operation data payload from the robot.

        Args:
            payload (bytes): The payload containing operation data.
        """
        with open(Files.BINARY_FILE, "ab") as f:
            f.write(payload)

        self._operation_data.update(payload)

        with open(Files.SENSOR_DATA, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    *self._operation_data.sensors,
                    self._operation_data.x,
                    self._operation_data.y,
                    self._operation_data.heading,
                ]
            )
