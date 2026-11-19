
from src.repositories.task_repository import TaskRepository

repository = TaskRepository()

print("TEST 1: Kiểm tra file JSON hiện tại")

try:
    tasks = repository.load_tasks()
    print("Đọc thành công!")
    print("Số công việc:", len(tasks))

except (ValueError, OSError) as error:
    print("Phát hiện lỗi:", error)


print("\nTEST 2: Kiểm tra JSON sai định dạng")

# Tạo file JSON thử nghiệm riêng
test_file = repository.file_path.parent / "invalid_test.json"

try:
    with open(test_file, "w", encoding="utf-8") as file:
        file.write("{ invalid json }")

    repository.file_path = test_file

    try:
        repository.load_tasks()
    except ValueError as error:
        print("Đã phát hiện JSON không hợp lệ:")
        print(error)

finally:
    if test_file.exists():
        test_file.unlink()
