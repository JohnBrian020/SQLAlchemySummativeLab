from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import (
    exercise_detail_schema,
    exercise_schema,
    exercises_schema,
    workout_detail_schema,
    workout_exercise_out_schema,
    workout_exercise_schema,
    workout_schema,
    workouts_schema,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)


def error(message, status):
    return jsonify({"errors": message}), status


def save(obj):
    """Add and commit an object, translating DB/model errors into responses."""
    try:
        db.session.add(obj)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return error([f"Database constraint violated: {e.orig}"], 400)
    except ValueError as e:
        db.session.rollback()
        return error([str(e)], 400)
    return None


# ---------- Workouts ----------

@app.get("/workouts")
def list_workouts():
    return jsonify(workouts_schema.dump(Workout.query.all())), 200


@app.get("/workouts/<int:id>")
def show_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error(["Workout not found"], 404)
    return jsonify(workout_detail_schema.dump(workout)), 200


@app.post("/workouts")
def create_workout():
    try:
        data = workout_schema.load(request.get_json(silent=True) or {})
    except ValidationError as e:
        return error(e.messages, 422)
    try:
        workout = Workout(**data)
    except ValueError as e:
        return error([str(e)], 400)
    failure = save(workout)
    if failure:
        return failure
    return jsonify(workout_schema.dump(workout)), 201


@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error(["Workout not found"], 404)
    db.session.delete(workout)  # cascades to WorkoutExercises
    db.session.commit()
    return "", 204


# ---------- Exercises ----------

@app.get("/exercises")
def list_exercises():
    return jsonify(exercises_schema.dump(Exercise.query.all())), 200


@app.get("/exercises/<int:id>")
def show_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error(["Exercise not found"], 404)
    return jsonify(exercise_detail_schema.dump(exercise)), 200


@app.post("/exercises")
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json(silent=True) or {})
    except ValidationError as e:
        return error(e.messages, 422)
    try:
        exercise = Exercise(**data)
    except ValueError as e:
        return error([str(e)], 400)
    failure = save(exercise)
    if failure:
        return failure
    return jsonify(exercise_schema.dump(exercise)), 201


@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error(["Exercise not found"], 404)
    db.session.delete(exercise)  # cascades to WorkoutExercises
    db.session.commit()
    return "", 204


# ---------- Workout <-> Exercise ----------

@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout:
        return error(["Workout not found"], 404)
    if not exercise:
        return error(["Exercise not found"], 404)

    try:
        data = workout_exercise_schema.load(request.get_json(silent=True) or {})
    except ValidationError as e:
        return error(e.messages, 422)

    try:
        we = WorkoutExercise(workout=workout, exercise=exercise, **data)
    except ValueError as e:
        db.session.rollback()
        return error([str(e)], 400)
    failure = save(we)
    if failure:
        return failure
    return jsonify(workout_exercise_out_schema.dump(we)), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)