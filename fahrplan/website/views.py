from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from . import db
from .model import Section, Line, User

# from random import randrange
# from lorem_text import lorem


views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
def index():
    # lines = db.session.execute(
    #     select(
    #         Fahrtstrecke.bezeichnung,
    #         Fahrtstrecke.notiz,
    #         Fahrtstrecke.preis,
    #         # Fahrtstrecke.abschnitte)  # bool is not iterable
    #     ).select_from(Abschnitt).join(Abschnitt.fs_id)
    #     .order_by(Fahrtstrecke.id.desc())
    #     .limit(2)
    # )
    # print(lines.abschnitte)
    lines = Line.query.all()
    return render_template("index.html", user=current_user, lines=lines)


# fahrplan/<strecken_id> ????
@views.route("/fahrplan/", methods=["GET", "POST"])
@login_required
def fahrplan():
    text = "irgendwas"
    return render_template("fahrplan.html", user=current_user, text=text)


@views.route("/users/", methods=["GET"])
@login_required
def users():
    all_users = User.query.all()
    return render_template("users.html", user=current_user, users=all_users)


@views.route("/users/<int:user_id>/delete", methods=["GET"])
@login_required
def users_delete(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash("Benutzer entfernt!", category="success")
            return redirect(url_for("views.users"))


@views.route("/users/<int:user_id>", methods=["GET", "POST"])
@login_required
def users_update(user_id):
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        admin = request.form.get("admin")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email in Benutzung")
        elif len(email) < 4:
            flash("E-Mail zu kurz (<3)", category="error")
        elif len(first_name) < 2:
            flash("Name zu kurz (<1)", category="error")
        elif password1 != password2:
            flash("Pw stimmt nicht überein", category="error")
        elif len(password1) < 7:
            flash("PW zu kurz(<6)", category="error")
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                admin=admin,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Benutzer angelegt!", category="success")
            return redirect(url_for("views.users"))
    user = User.query.get(user_id)
    print(user)
    return render_template("users_c_u.html", current_user=current_user, user=user)


@views.route("/users/create", methods=["GET", "POST"])
@login_required
def users_create():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        admin = request.form.get("admin")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email in Benutzung")
        elif len(email) < 4:
            flash("E-Mail zu kurz (<3)", category="error")
        elif len(first_name) < 2:
            flash("Name zu kurz (<1)", category="error")
        elif password1 != password2:
            flash("Pw stimmt nicht überein", category="error")
        elif len(password1) < 3:
            flash("PW zu kurz(<3)", category="error")
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                admin=admin,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Benutzer angelegt!", category="success")
            return redirect(url_for("views.users"))
    # user = User.query.get(user_id)
    return render_template("users_c_u.html", current_user=current_user, user=False)
