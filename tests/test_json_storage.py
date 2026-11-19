
from src.services.task_manager import TaskManager

# Khởi tạo TaskManager
manager = TaskManager()

# Thêm một công việc mới
task = manager.add_task({
    "title": "Kiểm tra JSON Persistence",
    "duration_minutes": 60,
    "priority": "high"
})

print("Đã thêm công việc:")
print(task.to_dict())

print("\nDanh sách công việc hiện tại:")

for item in manager.get_all_tasks():
    print(item.to_dict())
