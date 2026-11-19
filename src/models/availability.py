
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Availability:
    weekday: int
    start_time: str
    end_time: str

    def __post_init__(self):
        if not isinstance(self.weekday, int) or isinstance(self.weekday, bool):
            raise ValueError("Thứ trong tuần phải là số nguyên.")

        if self.weekday < 0 or self.weekday > 6:
            raise ValueError("Thứ trong tuần phải nằm trong khoảng 0 đến 6.")

        try:
            start = datetime.strptime(self.start_time, "%H:%M")
            end = datetime.strptime(self.end_time, "%H:%M")
        except ValueError as error:
            raise ValueError(
                "Thời gian phải có định dạng HH:MM, ví dụ 08:30."
            ) from error

        if start >= end:
            raise ValueError(
                "Thời gian kết thúc phải sau thời gian bắt đầu."
            )

    def to_dict(self):
        return {
            "weekday": self.weekday,
            "start_time": self.start_time,
            "end_time": self.end_time
        }
