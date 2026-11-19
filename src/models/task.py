
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    deadline: str | None = None

    task_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    status: str = "pending"

    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def to_dict(self):
        """Chuyển Task thành dictionary."""

        return {
            "task_id": self.task_id,
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "deadline": self.deadline,
            "status": self.status,
            "created_at": self.created_at
        }
