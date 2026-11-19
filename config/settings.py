
from pathlib import Path

# Đường dẫn gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent

# Các thư mục dữ liệu
DATA_DIR = BASE_DIR / "data"  # thư mục lưu trữ dữ liệu
INPUT_DIR = DATA_DIR / "input"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = DATA_DIR / "reports"

# Thông tin ứng dụng
APP_NAME = "AI Workforce"
APP_VERSION = "0.1.0"
TIMEZONE = "Asia/Ho_Chi_Minh"

# Chế độ chạy (Bật chế độ phát triển và kiểm lỗi)
DEBUG = True
