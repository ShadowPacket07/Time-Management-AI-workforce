
from src.core.validators import validate_task_data


# Dữ liệu hợp lệ
valid_task = {
    "title": "Học Python",
    "duration_minutes": 90,
    "priority": "high",
    "deadline": "2026-11-20T18:00:00"
}

# Dữ liệu không hợp lệ
invalid_task = {
    "title": "",
    "duration_minutes": -30,
    "priority": "normal",
    "deadline": "tomorrow"
}


# Kiểm tra dữ liệu hợp lệ
errors = validate_task_data(valid_task)

if not errors:
    print("Valid task: Dữ liệu hợp lệ!")
else:
    print("Valid task: Có lỗi!")
    for error in errors:
        print("-", error)

print("-" * 40)


# Kiểm tra dữ liệu không hợp lệ
errors = validate_task_data(invalid_task)

if not errors:
    print("Invalid task: Dữ liệu hợp lệ!")
else:
    print("Invalid task: Phát hiện lỗi!")
    for error in errors:
        print("-", error)
