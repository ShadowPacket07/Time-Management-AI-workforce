
from datetime import date, datetime, timedelta

from src.models.schedule_entry import ScheduleEntry


class SchedulingEngine:

    PRIORITY_ORDER = {
        "urgent": 0,
        "high": 1,
        "medium": 2,
        "low": 3
    }

    # Chuyển deadline thành datetime để so sánh
    def parse_deadline(self, deadline):

        if deadline is None:
            return None

        if not isinstance(deadline, str):
            raise ValueError("Deadline phải là chuỗi ngày giờ.")

        if len(deadline) == 10:
            try:
                parsed_date = date.fromisoformat(deadline)
            except ValueError as error:
                raise ValueError("Deadline không hợp lệ.") from error

            return datetime.combine(
                parsed_date,
                datetime.max.time()
            )

        try:
            parsed = datetime.fromisoformat(deadline)
        except ValueError as error:
            raise ValueError("Deadline không hợp lệ.") from error

        if parsed.tzinfo is not None:
            raise ValueError(
                "Deadline không được chứa múi giờ."
            )

        return parsed

    # Sắp xếp công việc theo deadline và priority
    def sort_tasks(self, tasks):

        pending_tasks = [
            task for task in tasks
            if task.status != "completed"
        ]

        def sort_key(task):

            deadline = self.parse_deadline(task.deadline)

            if deadline is None:
                return (
                    1,
                    datetime.max,
                    self.PRIORITY_ORDER.get(task.priority, 99)
                )

            return (
                0,
                deadline,
                self.PRIORITY_ORDER.get(task.priority, 99)
            )

        return sorted(pending_tasks, key=sort_key)

    # Tạo các khoảng thời gian rảnh lặp lại hàng tuần
    def generate_available_slots(
        self,
        availabilities,
        start_date,
        end_date
    ):

        if start_date > end_date:
            raise ValueError(
                "Ngày bắt đầu không được lớn hơn ngày kết thúc."
            )

        slots = []
        current_date = start_date

        while current_date <= end_date:

            for availability in availabilities:

                if current_date.weekday() != availability.weekday:
                    continue

                start_datetime = datetime.combine(
                    current_date,
                    datetime.strptime(
                        availability.start_time,
                        "%H:%M"
                    ).time()
                )

                end_datetime = datetime.combine(
                    current_date,
                    datetime.strptime(
                        availability.end_time,
                        "%H:%M"
                    ).time()
                )

                if end_datetime <= start_datetime:
                    raise ValueError(
                        "Thời gian kết thúc phải sau thời gian bắt đầu."
                    )

                slots.append({
                    "start": start_datetime,
                    "end": end_datetime
                })

            current_date += timedelta(days=1)

        slots.sort(key=lambda slot: slot["start"])

        # Kiểm tra các khoảng thời gian bị trùng
        latest_end = None

        for slot in slots:

            if latest_end is not None:
                if slot["start"] < latest_end:
                    raise ValueError(
                        "Phát hiện các khoảng thời gian rảnh bị trùng nhau."
                    )

            latest_end = max(
                latest_end,
                slot["end"]
            ) if latest_end is not None else slot["end"]

        return slots

    # Tạo lịch tự động
    def generate_schedule(
        self,
        tasks,
        availabilities,
        start_date,
        end_date,
        now=None
    ):

        if start_date > end_date:
            raise ValueError(
                "Ngày bắt đầu không được lớn hơn ngày kết thúc."
            )

        if now is None:
            now = datetime.now()

        if not isinstance(now, datetime):
            raise ValueError("now phải là kiểu datetime.")

        if now.tzinfo is not None:
            raise ValueError(
                "Tham số now phải là datetime không có múi giờ."
            )

        # Làm tròn thời điểm hiện tại lên phút tiếp theo
        # vì ScheduleEntry chỉ lưu giờ và phút
        if now.second > 0 or now.microsecond > 0:
            now = (
                now.replace(second=0, microsecond=0)
                + timedelta(minutes=1)
            )

        sorted_tasks = self.sort_tasks(tasks)

        slots = self.generate_available_slots(
            availabilities,
            start_date,
            end_date
        )

        scheduled = []
        unscheduled = []

        for task in sorted_tasks:

            if (
                not isinstance(task.duration_minutes, int)
                or isinstance(task.duration_minutes, bool)
                or task.duration_minutes <= 0
            ):
                raise ValueError(
                    f"Thời lượng công việc '{task.title}' không hợp lệ."
                )

            task_scheduled = False

            duration = timedelta(
                minutes=task.duration_minutes
            )

            deadline = self.parse_deadline(task.deadline)

            for slot in slots:

                slot_start = slot["start"]
                slot_end = slot["end"]

                # Không sử dụng thời gian đã qua
                if slot_end <= now:
                    continue

                actual_start = max(slot_start, now)

                task_end = actual_start + duration

                # Không đủ thời gian liên tục
                if task_end > slot_end:
                    continue

                # Không thể hoàn thành trước deadline
                if deadline is not None and task_end > deadline:
                    continue

                entry = ScheduleEntry(
                    task_id=task.task_id,
                    title=task.title,
                    date=actual_start.strftime("%Y-%m-%d"),
                    start_time=actual_start.strftime("%H:%M"),
                    end_time=task_end.strftime("%H:%M")
                )

                scheduled.append(entry)

                # Cập nhật thời gian còn lại
                slot["start"] = task_end

                task_scheduled = True
                break

            if not task_scheduled:
                unscheduled.append(task)

        return {
            "scheduled": scheduled,
            "unscheduled": unscheduled
        }
