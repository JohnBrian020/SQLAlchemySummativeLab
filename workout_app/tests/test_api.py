import unittest

from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise


class WorkoutAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

        cls.app_context = app.app_context()
        cls.app_context.push()

        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()

    def create_workout(self):
        response = self.client.post(
            "/workouts",
            json={
                "date": "2026-10-30",
                "duration_minutes": 45,
                "notes": "Test workout"
            }
        )
        return response.get_json()["id"]

    def create_exercise(self):
        response = self.client.post(
            "/exercises",
            json={
                "name": "Push-ups",
                "category": "strength",
                "equipment_needed": False
            }
        )
        return response.get_json()["id"]

    def test_get_workouts(self):
        response = self.client.get("/workouts")
        self.assertEqual(response.status_code, 200)

    def test_create_workout(self):
        response = self.client.post(
            "/workouts",
            json={
                "date": "2026-10-30",
                "duration_minutes": 45,
                "notes": "Morning workout"
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_invalid_workout_duration(self):
        response = self.client.post(
            "/workouts",
            json={
                "date": "2026-10-30",
                "duration_minutes": -5
            }
        )
        self.assertEqual(response.status_code, 422)

    def test_create_exercise(self):
        response = self.client.post(
            "/exercises",
            json={
                "name": "Squats",
                "category": "strength",
                "equipment_needed": False
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_create_workout_exercise(self):
        workout_id = self.create_workout()
        exercise_id = self.create_exercise()

        response = self.client.post(
            f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
            json={"reps": 15, "sets": 3}
        )

        self.assertEqual(response.status_code, 201)

    def test_duplicate_workout_exercise(self):
        workout_id = self.create_workout()
        exercise_id = self.create_exercise()

        url = (
            f"/workouts/{workout_id}/exercises/"
            f"{exercise_id}/workout_exercises"
        )

        self.client.post(url, json={"reps": 15, "sets": 3})
        response = self.client.post(url, json={"reps": 10, "sets": 2})

        self.assertEqual(response.status_code, 400)

    def test_missing_workout(self):
        response = self.client.get("/workouts/999")
        self.assertEqual(response.status_code, 404)

    def test_delete_workout_cascades_associations(self):
        workout_id = self.create_workout()
        exercise_id = self.create_exercise()

        self.client.post(
            f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
            json={"reps": 15, "sets": 3}
        )

        response = self.client.delete(f"/workouts/{workout_id}")
        self.assertEqual(response.status_code, 204)

        remaining = WorkoutExercise.query.filter_by(
            workout_id=workout_id
        ).count()

        self.assertEqual(remaining, 0)


if __name__ == "__main__":
    unittest.main()
