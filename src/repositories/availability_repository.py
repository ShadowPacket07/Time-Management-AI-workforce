
import json

from config.settings import DATA_DIR
from src.models.availability import Availability


class AvailabilityRepository:

    def __init__(self):
        self.file_path = DATA_DIR / "availabilities.json"

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_availabilities(self, availabilities):

        data = [
            item.to_dict()
            for item in availabilities
        ]

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    def load_availabilities(self):

        if not self.file_path.exists():
            return []

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "Dữ liệu thời gian rảnh phải là danh sách."
            )

        return [
            Availability(
                weekday=item["weekday"],
                start_time=item["start_time"],
                end_time=item["end_time"]
            )
            for item in data
        ]
