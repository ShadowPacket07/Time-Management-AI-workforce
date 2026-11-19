
import json

from config.settings import DATA_DIR
from src.models.schedule_entry import ScheduleEntry


class ScheduleRepository:

    def __init__(self):
        self.file_path = DATA_DIR / "schedules.json"

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_schedules(self, schedules):
        data = [
            schedule.to_dict()
            for schedule in schedules
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

    def load_schedules(self):
        if not self.file_path.exists():
            return []

        try:
            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"File lịch không hợp lệ: {error}"
            ) from error

        if not isinstance(data, list):
            raise ValueError(
                "Dữ liệu lịch phải là một danh sách."
            )

        schedules = []

        for item in data:

            if not isinstance(item, dict):
                raise ValueError(
                    "Mỗi lịch phải là một dictionary."
                )

            required_fields = [
                "task_id",
                "title",
                "date",
                "start_time",
                "end_time"
            ]

            for field in required_fields:
                if field not in item:
                    raise ValueError(
                        f"Lịch bị thiếu trường: {field}"
                    )

            schedules.append(
                ScheduleEntry(
                    task_id=item["task_id"],
                    title=item["title"],
                    date=item["date"],
                    start_time=item["start_time"],
                    end_time=item["end_time"]
                )
            )

        return schedules
