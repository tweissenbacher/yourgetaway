import datetime
from flask import Flask, session, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
from security import authenticate
from models.userModel import UserModel
from helpers.sessionHelper import SessionHelper
from helpers.dateHelper import DateHelper

# takes care of user login
def login():
    session.clear()
    if request.method == "POST":
        email =request.form.get("email")
        password= request.form.get("password")
        user = authenticate(email, password)
        if user:
            session.update({"email": email})
            user.check_if_admin()
            if user.is_admin:
                return redirect ("/aktionen/neu")
            return redirect("/tickets/neu")
        flash("Inkorrekte Email und/oder inkorrektes Passwort.\nVersuchen Sie es erneut oder registrieren Sie sich, wenn Sie noch keinen Account haben.")
    return render_template("login.html", email = session.get("email"))

# takes care of user registration
def register():
    today = DateHelper.get_today()
    if request.method == "POST":
        email =request.form.get("email")
        password = request.form.get("password")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        birthday = request.form.get("birthday")
        if birthday:
            birthday = birthday.replace("T", " ")
            if birthday > today:
                flash("Das Geburtsdatum darf nicht in der Zukunft liegen.")
                return render_template("register.html", email=session.get("email"), today=today)
        user = UserModel.find_by_email(email)
        if user is None:
            UserModel.save_to_db(UserModel(email, password, firstname, lastname, '', birthday))
            flash("Registrierung erfolgreich! Sie können sich nun einloggen.")
            return redirect("/")
        flash("Es gibt bereits einen User mit dieser Email-Adresse. Bitte loggen Sie sich ein oder wählen Sie eine andere Emailadresse.")
    return render_template("register.html", email = session.get("email"), today = today)

# takes care of adaptations to user profile
def profilEditieren():
    if session.get("email") is None:
        return redirect ("/")
    user = UserModel.find_by_email(session.get("email"))
    user.check_if_admin()
    is_admin = user.is_admin
    today = DateHelper.get_today()

    if request.method == "POST":
        password = request.form.get("password")
        if authenticate(user.email, password):
            password_new = request.form.get("new-password")
            if password_new and password_new == password:
                flash("Das neue Passwort darf nicht dasselbe wie das alte Passwort sein. Versuchen Sie es noch einmal.")
            else:
                firstname = request.form.get("firstname")
                lastname = request.form.get("lastname")
                birthday = request.form.get("geburtsdatum")
                if birthday:
                    birthday = birthday.replace("T", " ")
                    if birthday > today:
                        flash("Das Geburtsdatum darf nicht in der Zukunft liegen.")
                        return render_template("profil.html", email=session.get("email"), is_admin=is_admin, user=user,
                                               today=today)
                if password_new:
                    password_new_hashed = generate_password_hash(password_new)
                    user.password = password_new_hashed
                user.firstname = firstname
                user.lastname = lastname
                user.birthday = birthday

                UserModel.save_to_db(user)
                flash("Profil erfolgreich editiert.")
        else:
            flash("Falsches Passwort. Versuchen Sie es noch einmal.")
    return render_template("profil.html", email=session.get("email"), is_admin = is_admin, user=user, today = today)

# takes care of log out
def ausloggen():
    session.clear()
    flash("Erfolgreich ausgeloggt.")
    return redirect("/")
