
from datetime import date

from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise


def seed_database():
    with app.app_context():
        # Clear existing records before seeding
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        db.session.commit()

        # Create exercises
        pushups = Exercise(
            name="Push-ups",
            category="strength",
            equipment_needed=False
        )

        squats = Exercise(
            name="Squats",
            category="strength",
            equipment_needed=False
        )

        running = Exercise(
            name="Running",
            category="cardio",
            equipment_needed=False
        )

        yoga = Exercise(
            name="Yoga",
            category="flexibility",
            equipment_needed=False
        )

        db.session.add_all([pushups, squats, running, yoga])
        db.session.flush()

        # Create workouts
        workout1 = Workout(
            date=date(2026, 10, 28),
            duration_minutes=45,
            notes="Upper body and leg workout"
        )

        workout2 = Workout(
            date=date(2026, 10, 29),
            duration_minutes=30,
            notes="Cardio and flexibility session"
        )

        db.session.add_all([workout1, workout2])
        db.session.flush()

        # Connect exercises to workouts
        workout_exercises = [
            WorkoutExercise(
                workout=workout1,
                exercise=pushups,
                reps=15,
                sets=3
            ),
            WorkoutExercise(
                workout=workout1,
                exercise=squats,
                reps=20,
                sets=3
            ),
            WorkoutExercise(
                workout=workout2,
                exercise=running,
                duration_seconds=1200
            ),
            WorkoutExercise(
                workout=workout2,
                exercise=yoga,
                duration_seconds=600
            )
        ]

        db.session.add_all(workout_exercises)
        db.session.commit()

        print("Database seeded successfully!")
        print(f"Exercises: {Exercise.query.count()}")
        print(f"Workouts: {Workout.query.count()}")
        print(f"Workout exercises: {WorkoutExercise.query.count()}")


if __name__ == "__main__":
    seed_database()
