
from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates,
    validates_schema
)

from server.models import ALLOWED_CATEGORIES


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Name cannot be blank.")

    @validates("category")
    def validate_category(self, value, **kwargs):
        if value.strip().lower() not in ALLOWED_CATEGORIES:
            raise ValidationError(
                f"Category must be one of: {', '.join(sorted(ALLOWED_CATEGORIES))}."
            )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True,
        strict=True,
        validate=validate.Range(min=1, max=600)
    )
    notes = fields.Str(
        allow_none=True,
        validate=validate.Length(max=1000)
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(
        allow_none=True,
        strict=True,
        validate=validate.Range(min=1)
    )
    sets = fields.Int(
        allow_none=True,
        strict=True,
        validate=validate.Range(min=1)
    )
    duration_seconds = fields.Int(
        allow_none=True,
        strict=True,
        validate=validate.Range(min=1)
    )

    @validates_schema
    def require_one_measure(self, data, **kwargs):
        if all(
            data.get(key) is None
            for key in ("reps", "sets", "duration_seconds")
        ):
            raise ValidationError(
                "Provide at least one of reps, sets, or duration_seconds.",
                "_schema"
            )


class WorkoutExerciseForWorkoutSchema(WorkoutExerciseSchema):
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutExerciseForExerciseSchema(WorkoutExerciseSchema):
    workout = fields.Nested(WorkoutSchema, dump_only=True)


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(
        WorkoutExerciseForWorkoutSchema,
        many=True,
        dump_only=True
    )


class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.Nested(
        WorkoutExerciseForExerciseSchema,
        many=True,
        dump_only=True
    )


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()

workout_exercise_schema = WorkoutExerciseSchema()

# Used when returning a newly created workout-exercise association
workout_exercise_out_schema = WorkoutExerciseForWorkoutSchema()
