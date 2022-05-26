import json
import os
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from . import db
from .model import Section, Line, User

# from random import randrange
# from lorem_text import lorem


views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
def index():
    lines = Line.query.all()
    return render_template("index.html", user=current_user, lines=lines)







# #@admin_required  #?? custom decorator ??
# # TODO: fahrplan/<strecken_id> ????
# @views.route("/lines/", methods=["GET", "POST"])
# @login_required
# def fahrplan():
#     lines = Line.query.all()
#     return render_template("lines.html", user=current_user, lines=lines)

# @views.route("/lines/create/<route_name>", methods=["GET", "POST"])
# @login_required
# def fahrtstrecke_create():
#     if request.method == "POST":
#         pass
#     base = os.environ.get("STRECKEN_API_BASE_URL")
#     url = f"{base}/page/2"
#     res = requests.get(url)
#     # data = res.json()
#     data = json.loads(res.content)
#     routes = data['items']
#     # return data
#     return render_template("lines_c.html", user=current_user, routes=routes)






# @views.route("/users/", methods=["GET"])
# @login_required
# def users():
#     all_users = User.query.all()
#     return render_template("users.html", user=current_user, users=all_users)


# @views.route("/users/<int:user_id>/delete", methods=["GET"])
# @login_required
# def users_delete(user_id):
#     user = User.query.get(user_id)
#     if user:
#         db.session.delete(user)
#         db.session.commit()
#         flash("Benutzer entfernt!", category="success")
#         return redirect(url_for("views.users"))


# @views.route("/users/<int:user_id>", methods=["GET", "POST"])
# @login_required
# def users_update(user_id):
#     if request.method == "POST":
#         email = request.form.get("email")
#         first_name = request.form.get("firstName")
#         last_name = request.form.get("lastName")
#         password1 = request.form.get("password1")
#         password2 = request.form.get("password2")
#         admin = request.form.get("admin")
#         old_pw = request.form.get("oldPW")

#         user = User.query.get(user_id)
#         print(password2)

#         if not user:
#             flash("User nicht vorhanden")
#         elif len(email) < 4:
#             flash("E-Mail zu kurz (<3)", category="error")
#         elif len(first_name) < 2:
#             flash("Name zu kurz (<2)", category="error")
#         elif len(last_name) < 2:
#             flash("Name zu kurz (<2)", category="error")
#         elif current_user.admin == 0:
#             if check_password_hash(user.password, old_pw) != True:
#                 flash("Aktuelles Passwort falsch!", category="error")
#                 # return redirect(request.referrer)
#                 # ?
#         elif (
#             password1 == None or password1 == "" and password2 == ""
#         ):  # pw fields empty
#             print("lolll")
#             user.update(email, first_name, last_name, admin)
#             db.session.commit()
#             flash("Benutzer bearbeitet!", category="success")
#             # return redirect(url_for("views.users"))
#             return redirect(request.referrer)

#         elif password1 != password2:
#             flash("Pw stimmt nicht überein", category="error")
#         elif len(password1) < 3:
#             flash("PW zu kurz(<3)", category="error")
#             # return redirect(request.referrer)
#         else:
#             user.update(
#                 email,
#                 first_name,
#                 last_name,
#                 admin,
#                 generate_password_hash(password1, method="sha256"),
#             )
#             db.session.commit()
#             flash("Benutzer bearbeitet!", category="success")
#             # return redirect(url_for("views.users"))
#             return redirect(request.referrer)
#     user = User.query.get(user_id)
#     print(user)
#     return render_template("users_c_u.html", current_user=current_user, user=user)


# @views.route("/users/create", methods=["GET", "POST"])
# @login_required
# def users_create():
#     if request.method == "POST":
#         email = request.form.get("email")
#         first_name = request.form.get("firstName")
#         last_name = request.form.get("lastName")
#         password1 = request.form.get("password1")
#         password2 = request.form.get("password2")
#         admin = request.form.get("admin")

#         user = User.query.filter_by(email=email).first()
#         # print(user.email == email)
#         if user:
#             flash("Email in Benutzung")
#         elif len(email) < 4:
#             flash("E-Mail zu kurz (<3)", category="error")
#         elif len(first_name) < 2:
#             flash("Name zu kurz (<1)", category="error")
#         elif password1 != password2:
#             flash("Pw stimmt nicht überein", category="error")
#         elif len(password1) < 3:
#             flash("PW zu kurz(<3)", category="error")
#         else:
#             new_user = User(
#                 email=email,
#                 first_name=first_name,
#                 last_name=last_name,
#                 admin=admin,
#                 password=generate_password_hash(password1, method="sha256"),
#             )
#             db.session.add(new_user)
#             db.session.commit()
#             flash("Benutzer angelegt!", category="success")
#         return redirect(request.referrer)
#         # return redirect(url_for("views.users"))
#     # user = User.query.get(user_id)
#     return render_template("users_c_u.html", current_user=current_user, user=False)
