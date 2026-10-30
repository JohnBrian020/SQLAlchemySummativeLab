# Workout Application Backend

A RESTful API backend for managing workouts, exercises, and the exercises performed during each workout. Built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow.

## Features

- Create, retrieve, and delete workouts.
- Create, retrieve, and delete exercises.
- Associate exercises with workouts.
- Track repetitions, sets, and exercise duration.
- Serialize nested workout and exercise data.
- Validate incoming data using Marshmallow.
- Enforce database constraints and model validations.
- Automatically remove workout-exercise associations when a workout or exercise is deleted.

## Technologies

- Python 3.8
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- SQLAlchemy
- Marshmallow 3.20.1
- SQLite

## Project Structure

```text
workout_app/
├── server/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   └── schemas.py
├── migrations/
├── tests/
│   └── test_api.py
├── seed.py
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Installation

Clone the repository and enter the project directory.

Install dependencies:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

## Database Setup

Initialize migrations if they have not already been initialized:

```bash
flask --app server.app db init
```

Create and apply migrations:

```bash
flask --app server.app db migrate -m "Create workout application tables"
flask --app server.app db upgrade
```

Seed the database:

```bash
python seed.py
```

## Running the Application

Start the Flask development server:

```bash
flask --app server.app run --port 5555
```

The API will be available at:

`http://127.0.0.1:5555`

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | Retrieve all workouts |
| GET | `/workouts/<id>` | Retrieve one workout |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |

### Exercises

| Method | Endpoint | Description |
|---|---|---|
| GET | `/exercises` | Retrieve all exercises |
| GET | `/exercises/<id>` | Retrieve one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |

### Workout Exercises

| Method | Endpoint | Description |
|---|---|---|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Example Requests

### Create an Exercise

```json
{
  "name": "Push-ups",
  "category": "strength",
  "equipment_needed": false
}
```

Allowed categories:

- strength
- cardio
- flexibility

### Create a Workout

```json
{
  "date": "2026-10-30",
  "duration_minutes": 45,
  "notes": "Upper body training"
}
```

### Associate an Exercise with a Workout

```json
{
  "reps": 15,
  "sets": 3
}
```

At least one of `reps`, `sets`, or `duration_seconds` must be provided.

## Validation and Constraints

- Required text fields cannot be empty.
- Workout duration must be between 1 and 600 minutes.
- Exercise categories must be valid.
- Repetitions, sets, and exercise duration must be positive when supplied.
- A workout cannot contain the same exercise more than once.
- Database constraints protect important data relationships and values.

Invalid request data returns a validation error. Missing records return HTTP 404.

## Running Tests

Run the automated test suite:

```bash
pipenv run python -m unittest discover -s tests -v
```

The tests cover API operations, validation, duplicate associations, missing records, and cascading deletion.

## Author

John Brian Waweru

Full-Stack Software Engineering Student
