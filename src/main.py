
from datetime import date

from src.services.workforce_service import WorkforceService


WEEKDAYS = {
    "0": "Thứ Hai",
    "1": "Thứ Ba",
    "2": "Thứ Tư",
    "3": "Thứ Năm",
    "4": "Thứ Sáu",
    "5": "Thứ Bảy",
    "6": "Chủ Nhật"
}


def show_menu():
    print("\n========== AI WORKFORCE ==========")
    print("1. Thêm công việc")
    print("2. Xem danh sách công việc")
    print("3. Cập nhật công việc")
    print("4. Xóa công việc")
    print("5. Hoàn thành công việc")
    print("6. Thêm thời gian rảnh")
    print("7. Xem thời gian rảnh")
    print("8. Tạo lịch tự động")
    print("9. Xem lịch đã lưu")
    print("0. Thoát")
    print("==================================")


def update_task(service):

    task_id = input("Nhập Task ID: ")

    task = service.get_task_by_id(task_id)

    if task is None:
        print("Không tìm thấy công việc.")
        return

    print("Để trống nếu không muốn thay đổi.")

    title = input(f"Tên mới [{task.title}]: ")
    duration = input(
        f"Thời lượng mới [{task.duration_minutes}]: "
    )
    priority = input(
        f"Mức ưu tiên mới [{task.priority}]: "
    )
    deadline = input(
        f"Deadline mới [{task.deadline or 'Không có'}]: "
    )

    updates = {}

    if title.strip():
        updates["title"] = title

    if duration.strip():
        updates["duration_minutes"] = int(duration)

    if priority.strip():
        updates["priority"] = priority.strip().lower()

    if deadline.strip():
        updates["deadline"] = deadline

    if updates:
        service.update_task(task_id, updates)
        print("Đã cập nhật công việc.")
    else:
        print("Không có thay đổi.")


def delete_task(service):

    task_id = input("Nhập Task ID cần xóa: ")

    confirmation = input(
        "Bạn có chắc chắn muốn xóa? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Đã hủy.")
        return

    if service.delete_task(task_id):
        print("Đã xóa công việc.")
    else:
        print("Không tìm thấy công việc.")


def complete_task(service):

    task_id = input("Nhập Task ID: ")

    if service.complete_task(task_id):
        print("Đã hoàn thành công việc.")
    else:
        print("Không tìm thấy công việc.")


def add_task(service):

    title = input("Tên công việc: ")

    duration = int(
        input("Thời lượng (phút): ")
    )

    print("Mức ưu tiên: low / medium / high / urgent")

    priority = input("Ưu tiên: ").strip().lower()

    deadline = input(
        "Deadline (YYYY-MM-DDTHH:MM:SS), bỏ trống nếu không có: "
    ).strip()

    task_data = {
        "title": title,
        "duration_minutes": duration,
        "priority": priority,
        "deadline": deadline if deadline else None
    }

    task = service.add_task(task_data)

    print("Đã thêm:", task.title)


def show_tasks(service):

    tasks = service.get_tasks()

    if not tasks:
        print("Chưa có công việc.")
        return

    for index, task in enumerate(tasks, start=1):

        print(
            f"{index}. {task.title} | "
            f"{task.duration_minutes} phút | "
            f"{task.priority} | "
            f"{task.status} | "
            f"Deadline: {task.deadline}"
        )


def add_availability(service):

    print("\nCác ngày trong tuần:")

    for key, value in WEEKDAYS.items():
        print(f"{key}. {value}")

    weekday = int(
        input("Chọn thứ (0-6): ")
    )

    start_time = input("Giờ bắt đầu (HH:MM): ")
    end_time = input("Giờ kết thúc (HH:MM): ")

    service.add_availability(
        weekday,
        start_time,
        end_time
    )

    print("Đã thêm thời gian rảnh.")


def show_availabilities(service):

    availabilities = service.get_availabilities()

    if not availabilities:
        print("Chưa thiết lập thời gian rảnh.")
        return

    for index, item in enumerate(availabilities, start=1):

        weekday = WEEKDAYS[str(item.weekday)]

        print(
            f"{index}. {weekday}: "
            f"{item.start_time} - {item.end_time}"
        )


def generate_schedule(service):

    start_date = date.fromisoformat(
        input("Ngày bắt đầu (YYYY-MM-DD): ")
    )

    end_date = date.fromisoformat(
        input("Ngày kết thúc (YYYY-MM-DD): ")
    )

    result = service.generate_schedule(
        start_date,
        end_date
    )

    print("\n===== LỊCH ĐÃ TẠO =====")

    for item in result["scheduled"]:

        print(
            f"{item.date} | "
            f"{item.start_time}-{item.end_time} | "
            f"{item.title}"
        )

    print("\n===== CHƯA ĐƯỢC XẾP =====")

    for task in result["unscheduled"]:

        print(
            f"{task.title} | "
            f"{task.duration_minutes} phút"
        )
        report = service.analyze_schedule(
            result,
            start_date,
            end_date
        )

    print("\n===== AI ASSISTANT REPORT =====")

    print(
        "Công việc đã xếp:",
        report["total_scheduled"]
    )

    print(
        "Công việc chưa xếp:",
        report["total_unscheduled"]
    )

    for message in report["messages"]:

        if isinstance(message, str):
            print("-", message)

        else:
            print("\nCông việc:", message["task"])
            print("Nguyên nhân:", message["reason"])
            print("Đề xuất:", message["suggestion"])


def show_saved_schedules(service):

    schedules = service.get_saved_schedules()

    if not schedules:
        print("Chưa có lịch được lưu.")
        return

    for item in schedules:

        print(
            f"{item.date} | "
            f"{item.start_time}-{item.end_time} | "
            f"{item.title}"
        )


def main():

    service = WorkforceService()

    while True:

        show_menu()

        choice = input("Chọn chức năng: ").strip()

        try:

            if choice == "1":
                add_task(service)

            elif choice == "2":
                show_tasks(service)

            elif choice == "3":
                update_task(service)

            elif choice == "4":
                delete_task(service)

            elif choice == "5":
                complete_task(service)

            elif choice == "6":
                add_availability(service)

            elif choice == "7":
                show_availabilities(service)

            elif choice == "8":
                generate_schedule(service)

            elif choice == "9":
                show_saved_schedules(service)

            elif choice == "0":
                print("Đóng AI Workforce.")
                break

            else:
                print("Lựa chọn không hợp lệ.")

        except (ValueError, OSError) as error:
            print("Lỗi:", error)


if __name__ == "__main__":
    main()
