
from datetime import datetime, timedelta, time

from src.services.scheduling_engine import SchedulingEngine


class ScheduleAssistant:

    def __init__(self):
        self.engine = SchedulingEngine()

    # Phân tích tổng quan lịch
    def analyze_schedule(
        self,
        result,
        availabilities,
        start_date,
        end_date
    ):

        scheduled = result["scheduled"]
        unscheduled = result["unscheduled"]

        report = {
            "total_scheduled": len(scheduled),
            "total_unscheduled": len(unscheduled),
            "total_available_minutes": 0,
            "total_scheduled_minutes": 0,
            "utilization_rate": 0,
            "messages": []
        }

        # Tính tổng thời gian đã được sử dụng
        scheduled_minutes = sum(
            (
                datetime.strptime(item.end_time, "%H:%M")
                - datetime.strptime(item.start_time, "%H:%M")
            ).total_seconds() / 60
            for item in scheduled
        )

        report["total_scheduled_minutes"] = int(
            scheduled_minutes
        )

        # Kiểm tra thời gian rảnh
        if not availabilities:

            report["messages"].append({
                "type": "warning",
                "message": "Bạn chưa thiết lập thời gian rảnh."
            })

            return report

        slots = self.engine.generate_available_slots(
            availabilities,
            start_date,
            end_date
        )

        available_minutes = sum(
            (slot["end"] - slot["start"]).total_seconds() / 60
            for slot in slots
        )

        report["total_available_minutes"] = int(
            available_minutes
        )

        if available_minutes > 0:

            utilization_rate = (
                scheduled_minutes / available_minutes
            ) * 100

            report["utilization_rate"] = round(
                utilization_rate,
                2
            )

        # Phân tích mức độ sử dụng thời gian
        if available_minutes == 0:

            report["messages"].append({
                "type": "warning",
                "message": "Không có thời gian rảnh trong phạm vi ngày đã chọn."
            })

        elif report["utilization_rate"] >= 90:

            report["messages"].append({
                "type": "warning",
                "message": (
                    "Lịch của bạn đang sử dụng gần hết thời gian rảnh. "
                    "Hãy cân nhắc dành thêm thời gian nghỉ ngơi."
                )
            })
        elif report["utilization_rate"] < 30:

            report["messages"].append({
                "type": "info",
                "message": "Bạn còn nhiều thời gian rảnh chưa được sử dụng."
            })

        else:

            report["messages"].append({
                "type": "info",
                "message": (
                    "Mức độ sử dụng thời gian hiện tại tương đối hợp lý."
                )
            })

        # Nếu không có công việc chưa xếp
        if not unscheduled:

            report["messages"].append({
                "type": "success",
                "message": "Tất cả công việc đều đã được xếp lịch."
            })

            return report

        if not slots:

            report["messages"].append(
                "Không có khoảng thời gian rảnh phù hợp."
            )

            return report

        # Tìm khoảng thời gian rảnh dài nhất
        max_duration = max(
            (
                slot["end"] - slot["start"]
            ).total_seconds() / 60
            for slot in slots
        )

        # Phân tích từng công việc chưa được xếp
        for task in unscheduled:

            reason = ""
            suggestion = ""

            duration = task.duration_minutes

            deadline = self.engine.parse_deadline(
                task.deadline
            )

            # Trường hợp thời lượng quá dài
            if duration > max_duration:

                reason = (
                    "Thời lượng công việc dài hơn "
                    "khoảng thời gian rảnh dài nhất."
                )

                suggestion = (
                    "Hãy tăng thời gian rảnh hoặc giảm "
                    "thời lượng công việc nếu có thể."
                )

            else:

                can_fit = False

                for slot in slots:

                    task_end = (
                        slot["start"]
                        + timedelta(minutes=duration)
                    )

                    if task_end > slot["end"]:
                        continue

                    if deadline is not None and task_end > deadline:
                        continue

                    can_fit = True
                    break

                if not can_fit and deadline is not None:

                    reason = (
                        "Không có khoảng thời gian phù hợp "
                        "để hoàn thành trước deadline."
                    )

                    suggestion = (
                        "Hãy kiểm tra lại deadline hoặc "
                        "thêm thời gian rảnh trước hạn."
                    )

                else:

                    reason = (
                        "Các khoảng thời gian phù hợp có thể "
                        "đã được phân bổ cho công việc khác."
                    )

                    suggestion = (
                        "Hãy thêm thời gian rảnh hoặc xem xét "
                        "thứ tự ưu tiên và deadline."
                    )

            report["messages"].append({
                "task": task.title,
                "reason": reason,
                "suggestion": suggestion
            })

        return report
