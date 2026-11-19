
import unittest

from src.models.task import Task
from src.services.scheduling_engine import SchedulingEngine


class TestSchedulingPriority(unittest.TestCase):

    def setUp(self):
        self.engine = SchedulingEngine()

    def test_nearest_deadline_first(self):

        tasks = [
            Task(
                title="Task deadline xa",
                duration_minutes=60,
                priority="urgent",
                deadline="2026-11-25T18:00:00"
            ),
            Task(
                title="Task deadline gần",
                duration_minutes=60,
                priority="low",
                deadline="2026-11-20T18:00:00"
            )
        ]

        result = self.engine.sort_tasks(tasks)

        self.assertEqual(
            result[0].title,
            "Task deadline gần"
        )

    def test_priority_when_same_deadline(self):

        deadline = "2026-11-25T18:00:00"

        tasks = [
            Task("Task medium", 60, "medium", deadline),
            Task("Task urgent", 60, "urgent", deadline),
            Task("Task high", 60, "high", deadline),
            Task("Task low", 60, "low", deadline)
        ]

        result = self.engine.sort_tasks(tasks)

        expected = [
            "Task urgent",
            "Task high",
            "Task medium",
            "Task low"
        ]

        actual = [task.title for task in result]

        self.assertEqual(actual, expected)

    def test_no_deadline_goes_last(self):

        tasks = [
            Task("Task không deadline", 60, "urgent"),
            Task(
                "Task có deadline",
                60,
                "low",
                "2026-11-25T18:00:00"
            )
        ]

        result = self.engine.sort_tasks(tasks)

        self.assertEqual(
            result[-1].title,
            "Task không deadline"
        )

    def test_date_only_deadline(self):

        deadline = self.engine.parse_deadline(
            "2026-11-25"
        )

        self.assertEqual(
            deadline.strftime("%Y-%m-%d %H:%M:%S"),
            "2026-11-25 23:59:59"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
