
import unittest
from datetime import date

from src.models.task import Task
from src.models.availability import Availability
from src.services.recommendation_engine import RecommendationEngine


class TestRecommendationEngine(unittest.TestCase):

    def setUp(self):
        self.engine = RecommendationEngine()

        self.start_date = date(2026, 11, 23)
        self.end_date = date(2026, 11, 29)

        self.availabilities = [
            Availability(
                weekday=0,
                start_time="08:00",
                end_time="10:00"
            )
        ]

    def test_no_availability(self):
        result = {
            "scheduled": [],
            "unscheduled": []
        }

        recommendations = self.engine.generate_recommendations(
            result,
            [],
            self.start_date,
            self.end_date
        )

        self.assertEqual(len(recommendations), 1)
        self.assertEqual(
            recommendations[0]["type"],
            "availability"
        )

    def test_task_too_long(self):
        task = Task(
            title="Học Machine Learning",
            duration_minutes=180,
            priority="high"
        )

        result = {
            "scheduled": [],
            "unscheduled": [task]
        }

        recommendations = self.engine.generate_recommendations(
            result,
            self.availabilities,
            self.start_date,
            self.end_date
        )

        self.assertEqual(
            recommendations[0]["type"],
            "duration"
        )

        self.assertIn(
            "180 phút",
            recommendations[0]["detail"]
        )

    def test_task_with_deadline(self):
        task = Task(
            title="Học Python",
            duration_minutes=60,
            priority="high",
            deadline="2026-11-24T23:59:59"
        )

        result = {
            "scheduled": [],
            "unscheduled": [task]
        }

        recommendations = self.engine.generate_recommendations(
            result,
            self.availabilities,
            self.start_date,
            self.end_date
        )

        self.assertEqual(
            recommendations[0]["type"],
            "deadline"
        )

    def test_all_tasks_scheduled(self):
        result = {
            "scheduled": [object()],
            "unscheduled": []
        }

        recommendations = self.engine.generate_recommendations(
            result,
            self.availabilities,
            self.start_date,
            self.end_date
        )

        self.assertEqual(
            recommendations[0]["type"],
            "success"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
