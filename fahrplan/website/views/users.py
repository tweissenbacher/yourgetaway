import datetime
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from ..model import User

# from random import randrange
# from lorem_text import lorem


users = Blueprint("users", __name__)


@users.route("/users/", methods=["GET"])
@login_required
def users_view():
    all_users = User.query.all()
    all_users = sorted(all_users, key=lambda u: u.id)
    # all_users.sort()
    return render_template(
        "users/users.html", current_user=current_user, users=all_users
    )


@users.route("/users/<int:user_id>/trips", methods=["GET"])
@login_required
def user_trips(user_id):
    """View function to show all trips of a given User, 
    accepts URL parameter ?show=future to hide past trips"""
    
    show = request.args.get("show", default="all")  # future
    # sortby = request.args.get("sortby", default="date")  # line

    user = User.query.get(user_id)
    trips = user.trips

    resolved = []
    for trip in trips:
        resolved.extend(trip.get_resolved_all_dict())

    if show == "future":
        resolved = filter(lambda rt: rt["date"] >= datetime.date.today(), resolved)

    # if sortby == "line":
    #     resolved = sorted(resolved, key=lambda rt: rt["line"])
    # else:
    #     resolved = sorted(resolved, key=lambda rt: rt["date"])

    return render_template(
        "users/user_trips.html", current_user=current_user, resolved=resolved, user=user
    )


@users.route("/users/<int:user_id>/update", methods=["GET", "POST"])
@login_required
def user_update(user_id):
    """View function to update a given User"""
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        admin = request.form.get("admin")
        old_pw = request.form.get("oldPW")

        user = User.query.get(user_id)
        print(password2)

        if not user:
            flash("User nicht vorhanden")
        elif len(email) < 4:
            flash("E-Mail zu kurz (<3)", category="error")
        elif len(first_name) < 2:
            flash("Name zu kurz (<2)", category="error")
        elif len(last_name) < 2:
            flash("Name zu kurz (<2)", category="error")
        elif current_user.admin == 0:
            if check_password_hash(user.password, old_pw) != True:
                flash("Aktuelles Passwort falsch!", category="error")
                # return redirect(request.referrer)
                # ?
        elif (
            password1 == None or password1 == "" and password2 == ""
        ):  # pw fields empty
            user.update(email, first_name, last_name, admin)
            db.session.commit()
            flash("Benutzer bearbeitet!", category="success")
            return redirect(url_for("users.users"))
            # return redirect(request.referrer)

        elif password1 != password2:
            flash("Pw stimmt nicht überein", category="error")
        elif len(password1) < 3:
            flash("PW zu kurz(<3)", category="error")
            # return redirect(request.referrer)
        else:
            user.update(
                email,
                first_name,
                last_name,
                admin,
                generate_password_hash(password1, method="sha256"),
            )
            db.session.commit()
            flash("Benutzer bearbeitet!", category="success")
            # return redirect(url_for("users.users"))
            return redirect(request.referrer)
    user = User.query.get(user_id)
    print(user)
    return render_template("users/users_c_u.html", current_user=current_user, user=user)


@users.route("/users/create", methods=["GET", "POST"])
@login_required
def user_create():
    """View function to create a new User"""
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        admin = request.form.get("admin")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email in Benutzung", category="error")
            return redirect(request.referrer)
        elif len(email) < 4:
            flash("E-Mail zu kurz (<3)", category="error")
            return redirect(request.referrer)
        elif len(first_name) < 2:
            flash("Name zu kurz (<1)", category="error")
            return redirect(request.referrer)
        elif password1 != password2:
            flash("Pw stimmt nicht überein", category="error")
            return redirect(request.referrer)
        elif len(password1) < 3:
            flash("PW zu kurz(<3)", category="error")
            return redirect(request.referrer)
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
        return redirect(url_for("users.users_view"))
    return render_template(
        "users/users_c_u.html", current_user=current_user, user=False
    )


@users.route("/users/<int:user_id>/delete", methods=["GET"])
@login_required
def user_delete(user_id):
    """View function to delete a User"""
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Benutzer entfernt!", category="success")
        return redirect(url_for("users.users_view"))
    flash(f"Benutzer ID {user_id} nicht vorhanden!", category="error")
    return redirect(url_for("users.users_view"))
