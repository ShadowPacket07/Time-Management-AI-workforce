# AI Workforce – System Architecture

## 1. Tổng quan kiến trúc

Dự án sử dụng kiến trúc phân lớp (Layered Architecture), chia thành các tầng có nhiệm vụ riêng biệt.

## 2. Các tầng chính

### Presentation Layer
Vị trí: `src/dashboard.py`

Nhiệm vụ:
- Hiển thị giao diện Streamlit.
- Nhận dữ liệu từ người dùng.
- Gọi các phương thức từ WorkforceService.
- Hiển thị kết quả lập lịch và đề xuất.

### Service Layer
Vị trí: `src/services/`

Các thành phần:
- `WorkforceService`: Điều phối các nghiệp vụ.
- `TaskManager`: Quản lý công việc.
- `AvailabilityManager`: Quản lý thời gian rảnh.
- `SchedulingEngine`: Tạo lịch tự động.
- `ScheduleAssistant`: Phân tích lịch trình.
- `NaturalLanguageParser`: Phân tích yêu cầu tiếng Việt.
- `RecommendationEngine`: Đưa ra đề xuất điều chỉnh lịch.

### Repository Layer
Vị trí: `src/repositories/`

Nhiệm vụ:
- Đọc dữ liệu từ JSON.
- Ghi dữ liệu vào JSON.
- Quản lý quá trình lưu trữ.

### Model Layer
Vị trí: `src/models/`

Các model chính:
- Task
- Availability
- ScheduleEntry

### Core Layer
Vị trí: `src/core/`

Nhiệm vụ:
- Kiểm tra tính hợp lệ của dữ liệu.
- Chứa các thành phần xử lý nền tảng.

## 3. Luồng xử lý lập lịch

1. Người dùng nhập công việc và thiết lập thời gian rảnh.
2. Dashboard gửi yêu cầu đến WorkforceService.
3. WorkforceService lấy dữ liệu từ TaskManager và AvailabilityManager.
4. SchedulingEngine tạo lịch.
5. ScheduleRepository lưu kết quả.
6. ScheduleAssistant phân tích kết quả.
7. RecommendationEngine tạo đề xuất.
8. Dashboard hiển thị kết quả cho người dùng.

## 4. Nguyên tắc thiết kế

- Phân tách trách nhiệm giữa các tầng.
- Hạn chế xử lý nghiệp vụ trực tiếp trong giao diện.
- Tái sử dụng các service.
- Kiểm tra dữ liệu đầu vào.
- Có kiểm thử cho các thành phần quan trọng.
