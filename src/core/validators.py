
from datetime import datetime


def validate_task_data(task, allowed_priorities=None):
    """
    Kiểm tra tính hợp lệ của dữ liệu công việc.

    Trả về danh sách lỗi.
    Nếu danh sách rỗng, dữ liệu hợp lệ.
    """

    if allowed_priorities is None:
        allowed_priorities = [
            "low",
            "medium",
            "high",
            "urgent"
        ]

    errors = []

    # 1. Kiểm tra dữ liệu đầu vào
    if not isinstance(task, dict):
        return ["Dữ liệu công việc phải là dictionary."]

    # 2. Kiểm tra tiêu đề
    title = task.get("title")

    if not isinstance(title, str) or not title.strip():
        errors.append("Tiêu đề công việc không được để trống.")

    # 3. Kiểm tra thời lượng
    duration = task.get("duration_minutes")

    if (
        not isinstance(duration, int)
        or isinstance(duration, bool)
        or duration <= 0
    ):
        errors.append("Thời lượng phải là số nguyên dương.")

    # 4. Kiểm tra mức độ ưu tiên
    priority = task.get("priority")

    if priority not in allowed_priorities:
        errors.append(
            f"Mức ưu tiên không hợp lệ: {priority}"
        )

    # 5. Kiểm tra deadline (nếu có)

    deadline = task.get("deadline")

    if deadline is not None:

        if not isinstance(deadline, str):
            errors.append(
                "Deadline phải là chuỗi ngày giờ."
            )

        else:
            try:
                parsed_deadline = datetime.fromisoformat(deadline)

                if parsed_deadline.tzinfo is not None:
                    errors.append(
                        "Deadline không được chứa múi giờ. "
                        "Sử dụng giờ địa phương Asia/Ho_Chi_Minh."
                    )

            except ValueError:
                errors.append(
                    "Deadline phải có định dạng "
                    "YYYY-MM-DDTHH:MM:SS."
                )

    return errors
