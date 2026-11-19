
from datetime import date, datetime, time, timedelta

import streamlit as st
import calendar
from src.services.workforce_service import WorkforceService


# ==========================================
# 1. CẤU HÌNH DASHBOARD
# ==========================================

st.set_page_config(
    page_title="AI Workforce",
    page_icon="📅",
    layout="wide"
)

st.title("📅 AI Workforce")
st.caption("Personal Time Management & Scheduling System")


# ==========================================
# 2. KHỞI TẠO SERVICE
# ==========================================

@st.cache_resource
def get_workforce_service():
    return WorkforceService()


try:
    service = get_workforce_service()
except Exception as error:
    st.error(f"Không thể khởi tạo AI Workforce: {error}")
    st.stop()


# ==========================================
# 3. MENU ĐIỀU HƯỚNG
# ==========================================

menu = st.sidebar.radio(
    "Điều hướng",
    [
        "Dashboard",
        "Quản lý công việc",
        "Thời gian rảnh",
        "Lập lịch tự động",
        "Lịch tuần/tháng",
        "Nhập công việc bằng ngôn ngữ tự nhiên",
        "Lịch đã lưu"
    ]
)


# ==========================================
# 4. DASHBOARD TỔNG QUAN
# ==========================================

if menu == "Dashboard":

    st.header("Tổng quan")

    tasks = service.get_tasks()

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks
        if task.status == "completed"
    )

    pending_tasks = total_tasks - completed_tasks

    completion_rate = (
        completed_tasks / total_tasks * 100
        if total_tasks > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Tổng công việc", total_tasks)
    col2.metric("Đã hoàn thành", completed_tasks)
    col3.metric("Đang chờ", pending_tasks)
    col4.metric("Tiến độ", f"{completion_rate:.1f}%")

    st.subheader("Danh sách công việc")

    if tasks:

        task_data = [
            {
                "Tên công việc": task.title,
                "Thời lượng": task.duration_minutes,
                "Ưu tiên": task.priority,
                "Trạng thái": task.status,
                "Deadline": task.deadline or "Không có"
            }
            for task in tasks
        ]

        st.dataframe(
            task_data,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Tỷ lệ hoàn thành")

        st.progress(int(completion_rate))

    else:
        st.info("Bạn chưa có công việc nào.")
elif menu == "Nhập công việc bằng ngôn ngữ tự nhiên":
    st.title("Nhập công việc bằng ngôn ngữ tự nhiên")

    st.write(
        "Hãy mô tả công việc bằng tiếng Việt. "
        "Hệ thống sẽ tự động phân tích thông tin."
    )

    user_request = st.text_area(
        "Yêu cầu của bạn",
        placeholder=(
            "Ví dụ: Tôi cần học Python trong 2 tiếng, "
            "deadline ngày 25/11/2026, mức ưu tiên cao."
        ),
        height=120
    )

    if st.button("Phân tích yêu cầu"):
        try:
            parsed_task = service.natural_language_parser.parse(
                user_request
            )

            st.session_state["parsed_task"] = parsed_task
            st.success("Phân tích yêu cầu thành công!")

        except ValueError as error:
            st.session_state.pop("parsed_task", None)
            st.error(str(error))

    if "parsed_task" in st.session_state:
        parsed_task = st.session_state["parsed_task"]

        st.subheader("Thông tin công việc được nhận diện")

        st.write("**Tên công việc:**", parsed_task["title"])
        st.write(
            "**Thời lượng:**",
            f'{parsed_task["duration_minutes"]} phút'
        )
        st.write("**Mức ưu tiên:**", parsed_task["priority"])
        st.write(
            "**Deadline:**",
            parsed_task["deadline"] or "Chưa thiết lập"
        )

        if st.button("Xác nhận và thêm công việc"):
            try:
                task = service.task_manager.add_task(parsed_task)

                st.success(
                    f"Đã thêm công việc: {task.title}"
                )

                st.session_state.pop("parsed_task", None)

            except ValueError as error:
                st.error(str(error))

# ==========================================
# 5. QUẢN LÝ CÔNG VIỆC
# ==========================================

elif menu == "Quản lý công việc":

    st.header("Quản lý công việc")

    tab1, tab2 = st.tabs([
        "Thêm công việc",
        "Cập nhật / Xóa"
    ])

    # THÊM CÔNG VIỆC
    with tab1:

        with st.form("add_task_form"):

            title = st.text_input("Tên công việc")

            duration = st.number_input(
                "Thời lượng (phút)",
                min_value=1,
                value=60
            )

            priority = st.selectbox(
                "Mức ưu tiên",
                ["low", "medium", "high", "urgent"]
            )

            deadline_enabled = st.checkbox(
                "Thiết lập deadline"
            )

            deadline = None

            if deadline_enabled:

                deadline_date = st.date_input(
                    "Ngày deadline",
                    value=date.today()
                )

                deadline_time = st.time_input(
                    "Giờ deadline",
                    value=time(23, 59)
                )

                deadline = datetime.combine(
                    deadline_date,
                    deadline_time
                ).isoformat(timespec="seconds")

            submitted = st.form_submit_button(
                "Thêm công việc"
            )

            if submitted:

                try:

                    service.add_task({
                        "title": title,
                        "duration_minutes": int(duration),
                        "priority": priority,
                        "deadline": deadline
                    })

                    st.success("Đã thêm công việc.")
                    st.rerun()

                except (ValueError, OSError) as error:
                    st.error(str(error))

    # CẬP NHẬT VÀ XÓA
    with tab2:

        tasks = service.get_tasks()

        if not tasks:

            st.info("Chưa có công việc.")

        else:

            selected_id = st.selectbox(
                "Chọn công việc",
                options=[task.task_id for task in tasks],
                format_func=lambda task_id: next(
                    task.title
                    for task in tasks
                    if task.task_id == task_id
                )
            )

            selected_task = service.get_task_by_id(
                selected_id
            )

            if selected_task:

                st.write(
                    f"Trạng thái: {selected_task.status}"
                )

                with st.form("update_task_form"):

                    new_title = st.text_input(
                        "Tên công việc",
                        value=selected_task.title
                    )

                    new_duration = st.number_input(
                        "Thời lượng (phút)",
                        min_value=1,
                        value=selected_task.duration_minutes
                    )

                    new_priority = st.selectbox(
                        "Mức ưu tiên",
                        ["low", "medium", "high", "urgent"],
                        index=[
                            "low", "medium", "high", "urgent"
                        ].index(selected_task.priority)
                    )

                    new_deadline = st.text_input(
                        "Deadline (YYYY-MM-DDTHH:MM:SS)",
                        value=selected_task.deadline or "",
                        help="Để trống nếu muốn xóa deadline."
                    )

                    update_submitted = st.form_submit_button(
                        "Lưu thay đổi"
                    )

                    if update_submitted:

                        try:

                            service.update_task(
                                selected_id,
                                {
                                    "title": new_title,
                                    "duration_minutes": int(new_duration),
                                    "priority": new_priority,
                                    "deadline": (
                                        new_deadline.strip()
                                        if new_deadline.strip()
                                        else None
                                    )
                                }
                            )

                            st.success("Đã cập nhật công việc.")
                            st.rerun()

                        except (ValueError, OSError) as error:
                            st.error(str(error))

                col1, col2 = st.columns(2)

                if selected_task.status != "completed":

                    if col1.button(
                        "Hoàn thành công việc",
                        use_container_width=True
                    ):

                        service.complete_task(selected_id)
                        st.success("Đã hoàn thành.")
                        st.rerun()

                if col2.button(
                    "Xóa công việc",
                    use_container_width=True
                ):

                    service.delete_task(selected_id)
                    st.success("Đã xóa công việc.")
                    st.rerun()


# ==========================================
# 6. QUẢN LÝ THỜI GIAN RẢNH
# ==========================================

elif menu == "Thời gian rảnh":

    st.header("Quản lý thời gian rảnh")

    weekdays = {
        "Thứ Hai": 0,
        "Thứ Ba": 1,
        "Thứ Tư": 2,
        "Thứ Năm": 3,
        "Thứ Sáu": 4,
        "Thứ Bảy": 5,
        "Chủ Nhật": 6
    }

    with st.form("availability_form"):

        selected_day = st.selectbox(
            "Ngày trong tuần",
            list(weekdays.keys())
        )

        start_time = st.time_input(
            "Giờ bắt đầu",
            value=time(8, 0)
        )

        end_time = st.time_input(
            "Giờ kết thúc",
            value=time(12, 0)
        )

        submitted = st.form_submit_button(
            "Thêm thời gian rảnh"
        )

        if submitted:

            try:

                service.add_availability(
                    weekdays[selected_day],
                    start_time.strftime("%H:%M"),
                    end_time.strftime("%H:%M")
                )

                st.success("Đã thêm thời gian rảnh.")
                st.rerun()

            except (ValueError, OSError) as error:
                st.error(str(error))

    st.subheader("Thời gian rảnh đã thiết lập")

    availabilities = service.get_availabilities()

    if availabilities:

        availability_data = []

        for item in availabilities:

            day_name = next(
                name
                for name, number in weekdays.items()
                if number == item.weekday
            )

            availability_data.append({
                "Ngày": day_name,
                "Bắt đầu": item.start_time,
                "Kết thúc": item.end_time
            })

        st.dataframe(
            availability_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Bạn chưa thiết lập thời gian rảnh.")


# ==========================================
# 7. LẬP LỊCH TỰ ĐỘNG
# ==========================================

elif menu == "Lập lịch tự động":

    st.header("Tạo lịch tự động")

    st.write(
        "Scheduling Engine sẽ sắp xếp công việc "
        "dựa trên deadline và mức độ ưu tiên."
    )

    start_date = st.date_input(
        "Ngày bắt đầu",
        value=date.today()
    )

    end_date = st.date_input(
        "Ngày kết thúc",
        value=date.today() + timedelta(days=7)
    )

    if st.button(
        "Tạo lịch",
        type="primary"
    ):

        try:
            result = service.generate_schedule(
                start_date,
                end_date
            )

            st.success("Đã tạo lịch.")

            st.subheader("Công việc đã được xếp")

            scheduled_data = [
                {
                    "Ngày": item.date,
                    "Bắt đầu": item.start_time,
                    "Kết thúc": item.end_time,
                    "Công việc": item.title
                }
                for item in result["scheduled"]
            ]

            if scheduled_data:

                st.dataframe(
                    scheduled_data,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info("Chưa có công việc nào được xếp.")

            st.subheader("Công việc chưa được xếp")

            unscheduled_data = [
                {
                    "Công việc": task.title,
                    "Thời lượng": task.duration_minutes,
                    "Deadline": task.deadline or "Không có"
                }
                for task in result["unscheduled"]
            ]

            if unscheduled_data:

                st.dataframe(
                    unscheduled_data,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.success("Tất cả công việc đã được xếp.")

            report = service.analyze_schedule(
                result,
                start_date,
                end_date
            )

            st.subheader("Schedule Assistant")

            st.write(
                f"Đã xếp: {report['total_scheduled']}"
            )

            st.write(
                f"Chưa xếp: {report['total_unscheduled']}"
            )

            for message in report["messages"]:

                if message.get("type") == "success":
                    st.success(message["message"])

                elif message.get("type") == "warning":
                    st.warning(message["message"])

                elif message.get("type") == "info":
                    st.info(message["message"])

                else:
                    st.markdown(
                        f"**Công việc:** {message['task']}"
                    )

                    st.warning(
                        f"**Nguyên nhân:** {message['reason']}"
                    )

                st.info(
                    f"**Đề xuất:** {message['suggestion']}"
                )

            # =========================
            # RECOMMENDATION ENGINE
            # =========================

            st.subheader("Đề xuất điều chỉnh lịch thông minh")

            recommendations = service.generate_recommendations(
                result,
                start_date,
                end_date
            )

            if recommendations:

                for recommendation in recommendations:

                    recommendation_type = recommendation["type"]
                    title = recommendation["title"]
                    detail = recommendation["detail"]

                    if recommendation_type == "success":

                        st.success(f"**{title}**: {detail}")

                    elif recommendation_type == "availability":

                        st.warning(f"**{title}**: {detail}")

                    else:

                        with st.expander(title):

                            if "task_title" in recommendation:

                                st.write(
                                    "**Công việc:**",
                                    recommendation["task_title"]
                                )

                            st.write(detail)

            else:

                st.info("Hiện chưa có đề xuất điều chỉnh.")
        except (ValueError, OSError) as error:

            st.error(str(error))


# ==========================================
# 8. LỊCH ĐÃ LƯU
# ==========================================

elif menu == "Lịch đã lưu":

    st.header("Lịch đã lưu")

    schedules = service.get_saved_schedules()

    if schedules:

        schedule_data = [
            {
                "Ngày": item.date,
                "Bắt đầu": item.start_time,
                "Kết thúc": item.end_time,
                "Công việc": item.title
            }
            for item in schedules
        ]

        st.dataframe(
            schedule_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Chưa có lịch được lưu.")
