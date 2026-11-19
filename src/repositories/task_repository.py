
import json
from pathlib import Path

from config.settings import DATA_DIR


class TaskRepository:

    def __init__(self):
        self.file_path = DATA_DIR / "tasks.json"

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_tasks(self, tasks):
        data = [task.to_dict() for task in tasks]

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    def load_tasks(self):
        from src.models.task import Task

        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"File JSON không hợp lệ: {error}"
            ) from error

        except OSError as error:
            raise OSError(
                f"Không thể đọc file: {self.file_path}"
            ) from error

        if not isinstance(data, list):
            raise ValueError(
                "Dữ liệu JSON phải là một danh sách."
            )

        tasks = []

        required_fields = [
            "task_id",
            "title",
            "duration_minutes",
            "priority",
            "status",
            "created_at"
        ]

        for index, item in enumerate(data):

            if not isinstance(item, dict):
                raise ValueError(
                    f"Công việc tại vị trí {index} không phải dictionary."
                )

            missing_fields = [
                field for field in required_fields
                if field not in item
            ]

            if missing_fields:
                raise ValueError(
                    f"Công việc tại vị trí {index} thiếu trường: "
                    + ", ".join(missing_fields)
                )

            task = Task(
                title=item["title"],
                duration_minutes=item["duration_minutes"],
                priority=item["priority"],
                deadline=item.get("deadline"),
                task_id=item["task_id"],
                status=item["status"],
                created_at=item["created_at"]
            )

            tasks.append(task)

        return tasks
