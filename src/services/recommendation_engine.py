
from src.services.scheduling_engine import SchedulingEngine


class RecommendationEngine:

    def __init__(self):
        self.scheduling_engine = SchedulingEngine()

    def generate_recommendations(
        self,
        result,
        availabilities,
        start_date,
        end_date
    ):
        scheduled = result["scheduled"]
        unscheduled = result["unscheduled"]

        recommendations = []

        if not availabilities:
            recommendations.append({
                "type": "availability",
                "title": "Thiết lập thời gian rảnh",
                "detail": (
                    "Bạn chưa thiết lập thời gian rảnh. "
                    "Hãy thêm các khoảng thời gian rảnh "
                    "lặp lại hàng tuần."
                )
            })
            return recommendations

        slots = self.scheduling_engine.generate_available_slots(
            availabilities,
            start_date,
            end_date
        )

        if not slots:
            recommendations.append({
                "type": "date_range",
                "title": "Mở rộng phạm vi lập lịch",
                "detail": (
                    "Không tìm thấy khoảng thời gian rảnh "
                    "trong phạm vi ngày đã chọn."
                )
            })
            return recommendations

        longest_slot = max(
            (slot["end"] - slot["start"]).total_seconds() / 60
            for slot in slots
        )

        for task in unscheduled:

            if task.duration_minutes > longest_slot:
                recommendations.append({
                    "type": "duration",
                    "task_title": task.title,
                    "title": "Bổ sung khoảng thời gian liên tục",
                    "detail": (
                        f'Công việc "{task.title}" cần '
                        f"{task.duration_minutes} phút, nhưng "
                        f"khoảng thời gian rảnh dài nhất chỉ có "
                        f"{int(longest_slot)} phút."
                    )
                })

            elif task.deadline is not None:
                recommendations.append({
                    "type": "deadline",
                    "task_title": task.title,
                    "title": "Kiểm tra deadline",
                    "detail": (
                        f'Công việc "{task.title}" chưa được xếp lịch. '
                        "Hãy bổ sung thời gian rảnh trước deadline."
                    )
                })

            else:
                recommendations.append({
                    "type": "capacity",
                    "task_title": task.title,
                    "title": "Tăng khả năng đáp ứng lịch",
                    "detail": (
                        f'Công việc "{task.title}" chưa được xếp lịch. '
                        "Hãy bổ sung thời gian rảnh hoặc mở rộng "
                        "phạm vi ngày lập lịch."
                    )
                })

        if not unscheduled:
            recommendations.append({
                "type": "success",
                "title": "Lịch đã đáp ứng các công việc",
                "detail": (
                    f"Tất cả {len(scheduled)} công việc đều đã "
                    "được xếp lịch."
                )
            })

        return recommendations
