
import unittest
from datetime import date

from src.models.task import Task
from src.models.availability import Availability
from src.services.scheduling_engine import SchedulingEngine
from src.services.schedule_assistant import ScheduleAssistant


class TestScheduleAssistant(unittest.TestCase):

    def test_assistant_analyzes_unscheduled_task(self):

        engine = SchedulingEngine()
        assistant = ScheduleAssistant()

        task = Task(
            title="Học Python",
            duration_minutes=180,
            priority="high"
        )

        availabilities = [
            Availability(
                weekday=0,
                start_time="08:00",
                end_time="09:00"
            )
        ]

        result = engine.generate_schedule(
            [task],
            availabilities,
            date(2026, 11, 23),
            date(2026, 11, 23)
        )

        report = assistant.analyze_schedule(
            result,
            availabilities,
            date(2026, 11, 23),
            date(2026, 11, 23)
        )

        self.assertEqual(
            report["total_unscheduled"],
            1
        )

        task_messages = [
            message
            for message in report["messages"]
            if "task" in message
        ]

        self.assertEqual(
            len(task_messages),
            1
        )

        self.assertEqual(
            task_messages[0]["task"],
            "Học Python"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
