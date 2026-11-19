
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScheduleEntry:
    task_id: str
    title: str
    date: str
    start_time: str
    end_time: str

    def __post_init__(self):
        # Kiểm tra định dạng ngày
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError as error:
            raise ValueError(
                "Ngày phải có định dạng YYYY-MM-DD."
            ) from error

        # Kiểm tra định dạng giờ
        try:
            start = datetime.strptime(self.start_time, "%H:%M")
            end = datetime.strptime(self.end_time, "%H:%M")
        except ValueError as error:
            raise ValueError(
                "Giờ phải có định dạng HH:MM."
            ) from error

        if start >= end:
            raise ValueError(
                "Giờ kết thúc phải sau giờ bắt đầu."
            )

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time
        }
