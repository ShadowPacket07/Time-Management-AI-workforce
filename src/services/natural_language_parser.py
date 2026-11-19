
import re
from datetime import date, datetime


class NaturalLanguageParser:

    PRIORITY_KEYWORDS = {
        "urgent": ["khẩn cấp", "gấp", "cực kỳ quan trọng"],
        "high": ["cao", "ưu tiên cao", "quan trọng"],
        "medium": ["trung bình", "bình thường"],
        "low": ["thấp", "ưu tiên thấp", "không gấp"]
    }

    def parse(self, text, today=None):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Yêu cầu không được để trống.")

        if today is None:
            today = date.today()

        normalized_text = text.strip().lower()

        duration = self._extract_duration(normalized_text)
        deadline = self._extract_deadline(normalized_text, today)
        priority = self._extract_priority(normalized_text)
        title = self._extract_title(text, normalized_text)

        if duration is None:
            raise ValueError(
                "Không tìm thấy thời lượng. "
                "Ví dụ: trong 2 tiếng hoặc 90 phút."
            )

        if not title:
            raise ValueError("Không xác định được tên công việc.")

        return {
            "title": title,
            "duration_minutes": duration,
            "priority": priority,
            "deadline": deadline
        }

    def _extract_duration(self, text):
        pattern = (
            r"(?:trong\s*)?(\d+(?:[.,]\d+)?)\s*"
            r"(tiếng|giờ|phút|ngày)"
        )

        match = re.search(pattern, text)

        if not match:
            return None

        amount = float(match.group(1).replace(",", "."))
        unit = match.group(2)

        multipliers = {
            "tiếng": 60,
            "giờ": 60,
            "phút": 1,
            "ngày": 1440
        }

        duration = int(amount * multipliers[unit])

        if duration <= 0:
            raise ValueError("Thời lượng phải lớn hơn 0 phút.")

        return duration

    def _extract_deadline(self, text, today):
        patterns = [
            r"\b(\d{4}-\d{2}-\d{2})\b",
            r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b"
        ]

        for pattern in patterns:
            match = re.search(pattern, text)

            if not match:
                continue

            value = match.group(1)

            try:
                if "-" in value and len(value) == 10 and value[4] == "-":
                    parsed_date = date.fromisoformat(value)
                else:
                    normalized = value.replace("-", "/")
                    parsed_date = datetime.strptime(
                        normalized, "%d/%m/%Y"
                    ).date()
            except ValueError as error:
                raise ValueError("Ngày deadline không hợp lệ.") from error

            return f"{parsed_date.isoformat()}T23:59:59"

        if "ngày mai" in text:
            parsed_date = date.fromordinal(today.toordinal() + 1)
            return f"{parsed_date.isoformat()}T23:59:59"

        if "hôm nay" in text:
            return f"{today.isoformat()}T23:59:59"

        return None

    def _extract_priority(self, text):
        for priority, keywords in self.PRIORITY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return priority

        return "medium"

    def _extract_title(self, original_text, normalized_text):
        title = original_text.strip()

        # Bỏ phần mở đầu thường gặp.
        title = re.sub(
            r"^(tôi cần|tôi muốn|hãy|cần|muốn)\s+",
            "",
            title,
            flags=re.IGNORECASE
        )

        # Bỏ phần thời lượng và nội dung phía sau.
        title = re.split(
            r"\btrong\s+\d+(?:[.,]\d+)?\s*"
            r"(?:tiếng|giờ|phút|ngày)\b",
            title,
            maxsplit=1,
            flags=re.IGNORECASE
        )[0]

        # Bỏ phần deadline và mức ưu tiên.
        title = re.split(
            r",?\s*(?:deadline|hạn chót|hạn hoàn thành|"
            r"mức ưu tiên|ưu tiên)\b",
            title,
            maxsplit=1,
            flags=re.IGNORECASE
        )[0]

        title = title.strip(" ,.!?")

        return title
