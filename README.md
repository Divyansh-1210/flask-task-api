# Flask Task Manager API

A simple REST API built with Python, Flask, and SQLite. This project implements CRUD operations for a task management system and is a good starter backend project for GitHub.

## Features

- Create a task
- Read all tasks
- Read a single task
- Update a task
- Delete a task
- SQLite persistence with SQLAlchemy

## Setup

1. Open the project folder in your terminal.
2. Create and activate a Python virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Start the API server:

```powershell
python app.py
```

The API will run at `http://127.0.0.1:5000`.

## API Endpoints

### Get all tasks

- `GET /tasks`

### Get task by ID

- `GET /tasks/:id`

### Create a new task

- `POST /tasks`
- Body JSON:

```json
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "completed": false
}
```

### Update an existing task

- `PUT /tasks/:id`
- Body JSON can include any of:

```json
{
  "title": "Buy groceries and fruit",
  "description": "Milk, bread, eggs, apples",
  "completed": true
}
```

### Delete a task

- `DELETE /tasks/:id`

## Postman Collections

Import `postman_collection.json` into Postman to test all endpoints quickly.

## Notes for FastAPI Users

If you know FastAPI, the same CRUD patterns apply:

- use `@app.get`, `@app.post`, `@app.put`, and `@app.delete`
- validate request bodies with Pydantic models
- use SQLAlchemy or SQLite for persistence

This Flask version keeps the implementation minimal while showing REST API and database skills.
