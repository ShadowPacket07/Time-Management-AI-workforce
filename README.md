# AI Workforce – Intelligent Time Management System

**AI Workforce** là hệ thống quản lý thời gian và lập lịch công việc thông minh, được phát triển bằng Python và Streamlit. Dự án hỗ trợ người dùng quản lý công việc, thiết lập thời gian rảnh và tự động xây dựng lịch trình dựa trên deadline, mức độ ưu tiên và khả năng đáp ứng của quỹ thời gian.

**Version:** 0.1.0  
**Status:** Under Development  
**Language:** Python

---

## 1. Mục tiêu dự án

AI Workforce hướng đến việc hỗ trợ người dùng sử dụng thời gian hiệu quả hơn thông qua các mục tiêu:

- Quản lý danh sách công việc cá nhân.
- Thiết lập thời gian rảnh có tính lặp lại hàng tuần.
- Tự động sắp xếp lịch trình thực hiện công việc.
- Ưu tiên công việc có deadline gần nhất.
- Phân tích hiệu quả sử dụng thời gian.
- Tiếp nhận yêu cầu tạo công việc bằng ngôn ngữ tự nhiên.
- Đưa ra đề xuất cải thiện lịch trình khi công việc chưa được sắp xếp.

## 2. Công nghệ sử dụng

| Công nghệ | Vai trò |
|---|---|
| Python | Ngôn ngữ lập trình chính |
| Streamlit | Xây dựng giao diện ứng dụng |
| JSON | Lưu trữ dữ liệu |
| unittest | Kiểm thử phần mềm |
| YAML | Quản lý cấu hình lập lịch |

## 3. Chức năng chính

### 3.1. Quản lý công việc

- Thêm công việc mới.
- Xem danh sách công việc.
- Cập nhật thông tin công việc.
- Xóa công việc.
- Đánh dấu công việc đã hoàn thành.

### 3.2. Quản lý thời gian rảnh

- Thiết lập thời gian rảnh theo từng ngày trong tuần.
- Hỗ trợ lịch rảnh lặp lại hàng tuần.
- Kiểm tra các khoảng thời gian bị trùng lặp.

### 3.3. Lập lịch tự động

- Sắp xếp công việc theo deadline gần nhất.
- Ưu tiên mức độ quan trọng khi các công việc có cùng deadline.
- Không chia nhỏ công việc.
- Không xếp lịch vượt quá deadline.
- Không xếp lịch vào những khoảng thời gian đã qua.

### 3.4. Phân tích lịch trình

- Thống kê các công việc đã được xếp lịch.
- Phân tích các công việc chưa được xếp lịch.
- Đánh giá mức độ sử dụng thời gian rảnh.

### 3.5. Xử lý ngôn ngữ tự nhiên

Cho phép người dùng nhập yêu cầu bằng tiếng Việt để hệ thống phân tích và trích xuất thông tin:

- Tên công việc.
- Thời lượng thực hiện.
- Deadline.
- Mức độ ưu tiên.

### 3.6. Đề xuất điều chỉnh lịch trình

- Đề xuất bổ sung thời gian rảnh.
- Đề xuất mở rộng phạm vi lập lịch.
- Đề xuất bổ sung khoảng thời gian rảnh liên tục.
- Cảnh báo các công việc chưa được xếp lịch.

## 4. Cấu trúc dự án

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

## 5. Cài đặt và chạy dự án

### Yêu cầu

- Python 3.x
- Git
- pip

### Bước 1: Clone repository

```bash
git clone https://github.com/ShadowPacket07/Time-Management-AI-workforce.git
cd Time-Management-AI-workforce
```

### Bước 2: Tạo môi trường ảo

```bash
python -m venv .venv
```

### Bước 3: Kích hoạt môi trường ảo

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### Bước 4: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 5: Khởi chạy ứng dụng

```bash
python -m streamlit run src/dashboard.py
```

Sau khi khởi chạy thành công, Streamlit sẽ cung cấp địa chỉ truy cập ứng dụng trên trình duyệt.

## 6. Kiểm thử

Dự án sử dụng thư viện `unittest` để kiểm thử các thành phần.

Chạy toàn bộ bộ kiểm thử:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## 7. Nguyên lý hoạt động của thuật toán lập lịch

Scheduling Engine sử dụng chiến lược tham lam (Greedy Scheduling) với các bước chính:

1. Lọc các công việc chưa hoàn thành.
2. Sắp xếp công việc theo deadline gần nhất.
3. Nếu deadline bằng nhau, xét mức độ ưu tiên.
4. Sinh các khoảng thời gian rảnh dựa trên lịch rảnh hàng tuần.
5. Tìm khoảng thời gian liên tục đủ dài để thực hiện công việc.
6. Kiểm tra tính hợp lệ của khoảng thời gian so với deadline.
7. Tạo lịch cho các công việc đáp ứng điều kiện.
8. Đưa các công việc không thể xếp lịch vào danh sách chưa được sắp xếp.

## 8. Giới hạn hiện tại

- Dữ liệu được lưu trữ bằng JSON, chưa sử dụng hệ quản trị cơ sở dữ liệu chuyên dụng.
- Natural Language Parser sử dụng quy tắc và biểu thức chính quy (Regular Expressions).
- Recommendation Engine sử dụng các quy tắc đề xuất cơ bản.
- Thuật toán lập lịch sử dụng chiến lược tham lam (Greedy), chưa bảo đảm tìm được phương án tối ưu toàn cục.

## 9. Định hướng phát triển

- Tích hợp mô hình AI để cải thiện khả năng hiểu ngôn ngữ tự nhiên.
- Nghiên cứu và cải thiện thuật toán tối ưu lịch trình.
- Tích hợp hệ quản trị cơ sở dữ liệu.
- Bổ sung chức năng đăng nhập và quản lý nhiều người dùng.
- Tích hợp Google Calendar.
- Phát triển hệ thống báo cáo và thống kê nâng cao.

## 10. Phiên bản dự án

| Thuộc tính | Giá trị |
|---|---|
| Project | AI Workforce |
| Version | 0.1.0 |
| Status | Under Development |
| Language | Python |
| Interface | Streamlit |
