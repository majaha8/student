from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extension import db, login_manager
from app.model import Category, Task, User

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def index():
    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()  # get tasks from database
    completed = Task.query.filter_by(completed=True).count()  # count completed tasks
    return render_template(
        "index.html", user=current_user, tasks=tasks, completed=completed
    )


@main.route("/task")
@login_required
def task():
    categories = Category.query.all()  # get categories from database
    return render_template("task.html", categories=categories)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@main.route("/users")
def users():
    all_users = User.query.all()
    return render_template("users.html", users=all_users)


@main.route("/add-task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task_title = request.form.get("task_title", "").strip()
        category_id = request.form.get("category")  # dropdown sends ID now
        deadline_str = request.form.get("deadline")
        notes = request.form.get("notes")

        deadline = None
        if deadline_str:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")

        # Validation
        if not task_title:
            flash("Please enter something in the Task Title field.")
            return redirect(url_for("main.add_task"))
        if not category_id:
            flash("Please choose a Category.")
            return redirect(url_for("main.add_task"))

        # ✅ Get category object by ID
        category_obj = Category.query.get(int(category_id))
        if not category_obj:
            flash("Selected category does not exist.")
            return redirect(url_for("main.add_task"))

        # ✅ Create new task
        new_task = Task(
            task=task_title,
            category_id=category_obj.id,
            deadline=deadline,
            notes=notes,
            user_id=current_user.id,  # uncomment if Task has user_id
        )
        db.session.add(new_task)
        db.session.commit()

    flash("Task added successfully")
    return redirect(url_for("main.index"))


@main.route("/search", methods=["GET"])
def search():
    query = request.args.get("search", "").strip()
    tasks = Task.query.filter(
        Task.task.ilike(f"%{query}%"), Task.user_id == current_user.id
    ).all()
    return render_template("search.html", tasks=tasks)


@main.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete(task_id):
    task = db.session.get(Task, task_id)

    if not task:
        abort(404)

    db.session.delete(task)
    db.session.commit()
    print("task deleted")
    return redirect(url_for("main.index"))


@main.route("/update_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def update_task(task_id):

    task = db.session.get(Task, task_id)

    if not task:
        abort(404)

    if request.method == "POST":
        task.task = request.form.get("task", "")

        task.category_id = int(request.form.get("category", ""))

        deadline_str = request.form.get("deadline")

        if deadline_str:
            task.deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        else:
            task.deadline = None

        task.notes = request.form.get("notes")

        db.session.commit()

        return redirect(url_for("main.index"))

    categories = Category.query.all()

    return render_template("task.html", task=task, categories=categories)


@main.route("/toggle/<int:task_id>", methods=["POST"])
@login_required
def toggle(task_id):
    task = db.session.get(Task, task_id)

    if not task:
        abort(404)

    task.completed = not task.completed
    db.session.commit()

    return redirect(url_for("main.index"))
