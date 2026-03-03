from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.extension import db


# ====================the class start from here========================
class Task(db.Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    completed: Mapped[bool] = mapped_column(default=False)
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )
    deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)

    category = relationship("Category", back_populates="tasks")
    user: Mapped["User"] = relationship("User", backref="tasks")

    def __init__(
        self,
        task: str,
        user_id: int | None = None,
        category_id: int | None = None,
        deadline: datetime | None = None,
        notes: str | None = None,
    ):
        self.task = task
        self.user_id = user_id
        self.category_id = category_id
        self.deadline = deadline
        self.notes = notes


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    cat_name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    tasks = relationship("Task", back_populates="category")

    def __init__(self, cat_name: str):
        self.cat_name = cat_name


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def password_check(self, password):
        return check_password_hash(self.password, password)


"""
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

    tasks = relationship("Task", back_populates="user")

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def password_check(self, password):
        return check_password_hash(self.password, password)


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    cat_name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    tasks = relationship("Task", back_populates="category")


class Task(db.Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    completed: Mapped[bool] = mapped_column(default=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    deadline: Mapped[datetime | None] = mapped_column(DateTime)
    notes: Mapped[str | None] = mapped_column(String)

    category = relationship("Category", back_populates="tasks")
    user = relationship("User", back_populates="tasks")

"""
