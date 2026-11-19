
import yaml

from config.settings import BASE_DIR


# Đường dẫn đến file cấu hình YAML
SCHEDULING_RULES_PATH = (
    BASE_DIR / "config" / "scheduling_rules.yaml"
)


def load_scheduling_rules():
    """Đọc cấu hình lịch học từ file YAML."""

    if not SCHEDULING_RULES_PATH.exists():
        raise FileNotFoundError(
            f"Không tìm thấy file: {SCHEDULING_RULES_PATH}"
        )

    with open(
        SCHEDULING_RULES_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("File YAML không có cấu trúc hợp lệ.")

    validate_scheduling_rules(config)

    return config


def validate_scheduling_rules(config):
    """Kiểm tra cấu hình lịch học."""

    required_sections = [
        "schedule",
        "time_blocks",
        "rules",
        "priority"
    ]

    for section in required_sections:
        if section not in config:
            raise ValueError(
                f"Thiếu phần cấu hình: {section}"
            )

    duration = config["time_blocks"].get(
        "default_study_duration"
    )

    if not isinstance(duration, int) or duration <= 0:
        raise ValueError(
            "Thời lượng học phải là số nguyên dương."
        )

    return True


if __name__ == "__main__":

    rules = load_scheduling_rules()

    print("Đọc cấu hình thành công!")

    print("Múi giờ:", rules["schedule"]["timezone"])

    print(
        "Thời gian học mặc định:",
        rules["time_blocks"]["default_study_duration"],
        "phút"
    )

    print("Cấu hình hợp lệ:", validate_scheduling_rules(rules))
