
from src.models.task import Task
from src.core.validators import validate_task_data
from src.core.config_loader import load_scheduling_rules
from src.repositories.task_repository import TaskRepository


class TaskManager:

    def __init__(self):
        self.repository = TaskRepository()
        self.tasks = self.repository.load_tasks()

        rules = load_scheduling_rules()
        self.allowed_priorities = rules["priority"]["levels"]

    # Thêm công việc
    def add_task(self, task_data):

        errors = validate_task_data(
            task_data,
            self.allowed_priorities
        )

        if errors:
            raise ValueError("; ".join(errors))

        task = Task(
            title=task_data["title"].strip(),
            duration_minutes=task_data["duration_minutes"],
            priority=task_data["priority"],
            deadline=task_data.get("deadline")
        )

        self.tasks.append(task)

        self.repository.save_tasks(self.tasks)

        return task

    # Lấy tất cả công việc
    def get_all_tasks(self):
        return self.tasks.copy()

    # Tìm công việc theo ID
    def get_task_by_id(self, task_id):

        for task in self.tasks:

            if task.task_id == task_id:
                return task

        return None

    # Cập nhật công việc
    def update_task(self, task_id, updates):

        task = self.get_task_by_id(task_id)

        if task is None:
            raise ValueError("Không tìm thấy công việc.")

        if task.status == "completed":
            raise ValueError(
                "Không thể cập nhật công việc đã hoàn thành."
            )

        allowed_fields = {
            "title",
            "duration_minutes",
            "priority",
            "deadline"
        }

        if not isinstance(updates, dict):
            raise ValueError(
                "Dữ liệu cập nhật phải là dictionary."
            )

        invalid_fields = set(updates.keys()) - allowed_fields

        if invalid_fields:
            raise ValueError(
                "Trường cập nhật không hợp lệ: "
                + ", ".join(invalid_fields)
            )

        updated_data = task.to_dict()
        updated_data.update(updates)

        errors = validate_task_data(
            updated_data,
            self.allowed_priorities
        )

        if errors:
            raise ValueError("; ".join(errors))

        task.title = updated_data["title"].strip()
        task.duration_minutes = updated_data["duration_minutes"]
        task.priority = updated_data["priority"]
        task.deadline = updated_data.get("deadline")

        self.repository.save_tasks(self.tasks)

        return task

    # Xóa công việc
    def delete_task(self, task_id):

        task = self.get_task_by_id(task_id)

        if task is None:
            return False

        self.tasks.remove(task)

        self.repository.save_tasks(self.tasks)

        return True

    # Hoàn thành công việc
    def complete_task(self, task_id):

        task = self.get_task_by_id(task_id)

        if task is None:
            return False

        task.status = "completed"

        self.repository.save_tasks(self.tasks)

        return True
