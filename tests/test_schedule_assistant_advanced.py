
import unittest
from datetime import date

from src.models.task import Task
from src.models.availability import Availability
from src.services.scheduling_engine import SchedulingEngine
from src.services.schedule_assistant import ScheduleAssistant


class TestScheduleAssistantAdvanced(unittest.TestCase):

    def setUp(self):

        self.engine = SchedulingEngine()
        self.assistant = ScheduleAssistant()

        self.availabilities = [
            Availability(
                weekday=0,
                start_time="08:00",
                end_time="12:00"
            )
        ]

        self.start_date = date(2026, 11, 23)
        self.end_date = date(2026, 11, 23)

    def test_utilization_rate(self):

        task = Task(
            title="Học Python",
            duration_minutes=120,
            priority="high"
        )

        result = self.engine.generate_schedule(
            [task],
            self.availabilities,
            self.start_date,
            self.end_date,
            now=__import__("datetime").datetime(
                2026, 11, 22, 8, 0
            )
        )

        report = self.assistant.analyze_schedule(
            result,
            self.availabilities,
            self.start_date,
            self.end_date
        )

        self.assertEqual(
            report["total_available_minutes"],
            240
        )

        self.assertEqual(
            report["total_scheduled_minutes"],
            120
        )

        self.assertEqual(
            report["utilization_rate"],
            50
        )

    def test_unscheduled_task_analysis(self):

        task = Task(
            title="Học Machine Learning",
            duration_minutes=300,
            priority="high"
        )

        result = {
            "scheduled": [],
            "unscheduled": [task]
        }

        report = self.assistant.analyze_schedule(
            result,
            self.availabilities,
            self.start_date,
            self.end_date
        )

        self.assertEqual(
            report["total_unscheduled"],
            1
        )

        task_message = next(
            message
            for message in report["messages"]
            if isinstance(message, dict)
        )

        self.assertEqual(
            task_message["task"],
            "Học Machine Learning"
        )

        self.assertIn(
            "thời lượng",
            task_message["reason"].lower()
        )

    def test_no_availability(self):

        task = Task(
            title="Học SQL",
            duration_minutes=60,
            priority="medium"
        )

        report = self.assistant.analyze_schedule(
            {
                "scheduled": [],
                "unscheduled": [task]
            },
            [],
            self.start_date,
            self.end_date
        )

        self.assertEqual(
            report["total_available_minutes"],
            0
        )

        self.assertGreater(
            len(report["messages"]),
            0
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
