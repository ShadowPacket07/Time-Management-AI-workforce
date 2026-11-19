# AI Workforce – Intelligent Time Management System

## 1. Giới thiệu

**AI Workforce** là hệ thống quản lý thời gian và lập lịch công việc thông minh, hỗ trợ người dùng quản lý danh sách công việc, thiết lập thời gian rảnh và tự động sắp xếp lịch trình.

Hệ thống được xây dựng bằng Python và Streamlit, tập trung vào việc tối ưu thời gian thực hiện công việc dựa trên deadline, mức độ ưu tiên và thời gian rảnh của người dùng.

## 2. Mục tiêu dự án

- Quản lý công việc cá nhân.
- Quản lý thời gian rảnh lặp lại hàng tuần.
- Tự động lập lịch công việc.
- Ưu tiên công việc có deadline gần nhất.
- Phân tích hiệu quả sử dụng thời gian.
- Tiếp nhận yêu cầu tạo công việc bằng ngôn ngữ tự nhiên.
- Đưa ra đề xuất cải thiện lịch trình.

## 3. Công nghệ sử dụng

| Công nghệ | Vai trò |
|---|---|
| Python | Ngôn ngữ lập trình chính |
| Streamlit | Xây dựng giao diện |
| JSON | Lưu trữ dữ liệu |
| unittest | Kiểm thử phần mềm |
| YAML | Quản lý cấu hình |

## 4. Chức năng chính

### 4.1. Quản lý công việc
- Thêm công việc.
- Xem danh sách công việc.
- Cập nhật thông tin.
- Xóa công việc.
- Đánh dấu hoàn thành.

### 4.2. Quản lý thời gian rảnh
- Thiết lập thời gian rảnh theo thứ trong tuần.
- Lặp lại thời gian rảnh hàng tuần.
- Kiểm tra khoảng thời gian trùng lặp.

### 4.3. Lập lịch tự động
- Sắp xếp công việc theo deadline.
- Ưu tiên theo mức độ quan trọng khi deadline bằng nhau.
- Không chia nhỏ công việc.
- Không xếp lịch vượt quá deadline.
- Không xếp lịch vào thời gian đã qua.

### 4.4. Phân tích lịch trình
- Thống kê công việc đã được xếp lịch.
- Phân tích công việc chưa được xếp lịch.
- Đánh giá mức độ sử dụng thời gian rảnh.

### 4.5. Xử lý ngôn ngữ tự nhiên
Cho phép người dùng nhập yêu cầu bằng tiếng Việt để hệ thống trích xuất:
- Tên công việc.
- Thời lượng.
- Deadline.
- Mức độ ưu tiên.

### 4.6. Đề xuất điều chỉnh lịch
- Đề xuất bổ sung thời gian rảnh.
- Đề xuất mở rộng phạm vi lập lịch.
- Đề xuất bổ sung khoảng thời gian liên tục.
- Cảnh báo công việc chưa được xếp lịch.

## 5. Cấu trúc dự án

```text
AI-Workforce/
│
├── config/
│   ├── settings.py
│   └── scheduling_rules.yaml
│
├── data/
│   ├── input/
│   ├── processed/
│   ├── reports/
│   ├── tasks.json
│   ├── availabilities.json
│   └── schedules.json
│
├── src/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   └── dashboard.py
│
├── tests/
│
├── requirements.txt
└── README.md
```

## 6. Cài đặt và chạy dự án

### Bước 1: Clone repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-Workforce
```

### Bước 2: Tạo môi trường ảo

```bash
python -m venv .venv
```

### Bước 3: Kích hoạt môi trường

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Bước 4: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 5: Chạy ứng dụng

```bash
python -m streamlit run src/dashboard.py
```

## 7. Kiểm thử

Chạy toàn bộ bộ kiểm thử:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## 8. Thuật toán lập lịch

Scheduling Engine thực hiện các bước:

1. Lọc các công việc chưa hoàn thành.
2. Sắp xếp theo deadline gần nhất.
3. Nếu deadline bằng nhau, xét mức độ ưu tiên.
4. Sinh các khoảng thời gian rảnh theo tuần.
5. Tìm khoảng thời gian liên tục đủ dài.
6. Kiểm tra deadline.
7. Tạo lịch cho công việc phù hợp.
8. Đưa công việc không thể xếp lịch vào danh sách chưa được xếp lịch.

## 9. Giới hạn hiện tại

- Dữ liệu được lưu bằng JSON, chưa sử dụng cơ sở dữ liệu chuyên dụng.
- Bộ phân tích ngôn ngữ tự nhiên sử dụng quy tắc và biểu thức chính quy.
- Recommendation Engine sử dụng các quy tắc đề xuất cơ bản.
- Thuật toán lập lịch hiện tại sử dụng chiến lược tham lam (Greedy), chưa bảo đảm tìm được phương án tối ưu toàn cục.

## 10. Định hướng phát triển

- Tích hợp mô hình AI để hiểu yêu cầu ngôn ngữ tự nhiên tốt hơn.
- Cải thiện thuật toán tối ưu lịch trình.
- Tích hợp cơ sở dữ liệu.
- Bổ sung đăng nhập và quản lý nhiều người dùng.
- Tích hợp Google Calendar.
- Xây dựng báo cáo và thống kê nâng cao.

## 11. Phiên bản

**Project:** AI Workforce

**Version:** 0.1.0

**Status:** Under Development