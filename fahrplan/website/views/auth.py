from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from ..model import User


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "User needs to be logged in to view this page"
login_manager.login_message_category = "error"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """View function for login-page
    """    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Angemeldet", category="success")
                login_user(user)  # remember=True)
                return redirect(url_for("index.index_view"))
            else:
                flash("Passwort falsch", category="error")
        else:
            flash("User nicht vorhanden", category="error")
    if current_user.is_authenticated:
        flash(f"{current_user.first_name} Bereits angemeldet", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    """View function for user logout
    """    
    if current_user.id:
        logout_user()
        flash("Abgemeldet!", category="success")
    return redirect(url_for("auth.login"))


