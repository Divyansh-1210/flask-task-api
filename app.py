import os
from flask import Flask, request, jsonify, abort 
from flask_sqlalchemy import SQLAlchemy  
from datetime import datetime,timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


def init_db():
    with app.app_context():
        db.create_all()


if not os.path.exists("tasks.db"):
    init_db()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() + "Z",
        }


init_db()


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.order_by(Task.id).all()
    return jsonify([task.to_dict() for task in tasks])


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        abort(404, description="Task not found")
    return jsonify(task.to_dict())


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        abort(400, description="Title is required")

    task = Task(
        title=title,
        description=data.get("description"),
        completed=bool(data.get("completed", False)),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        abort(404, description="Task not found")

    data = request.get_json() or {}
    title = data.get("title")
    if title is not None:
        task.title = title
    if "description" in data:
        task.description = data.get("description")
    if "completed" in data:
        task.completed = bool(data.get("completed"))

    db.session.commit()
    return jsonify(task.to_dict())


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        abort(404, description="Task not found")

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error.description)}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error.description)}), 404


if __name__ == "__main__":
    app.run(debug=True)
