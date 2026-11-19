from src.services.task_manager import TaskManager


# Khởi tạo hệ thống
manager = TaskManager()


# 1. CREATE - Tạo công việc
task = manager.add_task({
    "title": "Học Python",
    "duration_minutes": 90,
    "priority": "high",
    "deadline": "2026-11-20T18:00:00"
})

print("1. CREATE")
print("Đã tạo:", task.to_dict())

task1 = manager.add_task({
    "title": "Ôn tập SQL",
    "duration_minutes": 60,
    "priority": "medium"
})

task2 = manager.add_task({
    "title": "Đọc tài liệu Linux",
    "duration_minutes": 45,
    "priority": "low"
})

print("\nKIỂM TRA DỮ LIỆU KHÔNG HỢP LỆ")

try:
    manager.add_task({
        "title": "Học Java",
        "duration_minutes": -10,
        "priority": "high"
    })

except ValueError as error:
    print("Phát hiện lỗi:", error)


# 2. READ - Hiển thị danh sách
print("\n2. READ")

for item in manager.get_all_tasks():
    print(item.to_dict())


# 3. UPDATE - Cập nhật công việc
print("\n3. UPDATE")

manager.update_task(
    task.task_id,
    {
        "title": "Học Python nâng cao",
        "duration_minutes": 120
    }
)

print("Sau khi cập nhật:", task.to_dict())


# 4. COMPLETE - Hoàn thành công việc
print("\n4. COMPLETE")

manager.complete_task(task.task_id)

print("Trạng thái:", task.status)


# 5. DELETE - Xóa công việc
print("\n5. DELETE")

result = manager.delete_task(task.task_id)

print("Xóa thành công:", result)

print("Số công việc còn lại:", len(manager.get_all_tasks()))
