from flask import Blueprint, flash, redirect, render_template, request, url_for

# from flask_login import login_required, login_user, logout_user
from app.extension import db
from app.model import Category

cat_bp = Blueprint("category", __name__)


@cat_bp.route("/")
def index():
    categories = Category.query.all()

    return render_template("category.html", categories=categories)


@cat_bp.route("/seed")
def seed_categories():
    # 1. Define the default categories
    print(">>>route being called")
    default_categories = ["Academic", "Personal", "Extracurricular", "Learning"]

    # 2. Get existing names from the database to prevent duplicates
    try:
        existing_categories = [c.cat_name for c in Category.query.all()]

        for cat_name in default_categories:
            if cat_name not in existing_categories:
                # Create a new Category instance using the name
                new_cat = Category(cat_name=cat_name)
                db.session.add(new_cat)

        # 3. Explicitly COMMIT the changes to save them
        db.session.commit()
        flash("Categories successfully added to the database!", "success")
        print("saved")
    except Exception as e:
        db.session.rollback()
        return f"Database error: {str(e)}"

    # 4. Redirect back to the task page so the new data can be loaded fresh
    return redirect(url_for("category.index"))
