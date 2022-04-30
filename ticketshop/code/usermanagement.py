from flask import Flask, session, render_template, request, redirect, flash
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate
from models.userModel import UserModel



def login():
    if request.method == "POST":
        email =request.form.get("email")
        password= request.form.get("password")
        user = authenticate(email, password)
        if user:
            session.update({"email": email})
            user.check_if_admin()
            if user.ist_admin:
                return redirect ("/aktionen/neu")
            return redirect("/tickets/neu")
        flash("Inkorrekte Email und/oder inkorrektes Passwort.\nVersuchen Sie es erneut oder registrieren Sie sich, wenn Sie noch keinen Account haben.")
    return render_template("login.html", email = session.get("email"))

def register():
    if request.method == "POST":
        email =request.form.get("email")
        password = request.form.get("password")
        vorname = request.form.get("vorname")
        nachname = request.form.get("nachname")
        geburtsdatum = request.form.get("geburtsdatum")
        if geburtsdatum:
            geburtsdatum = geburtsdatum.replace("T", " ")
        user = UserModel.find_by_email(email)
        if user is None:
            UserModel.save_to_db(UserModel(email, password, vorname, nachname, '', geburtsdatum))
            flash("Registrierung erfolgreich! Sie können sich nun einloggen.")
            return redirect("/")
        flash("Es gibt bereits einen User mit dieser Email-Adresse. Bitte loggen Sie sich ein oder wählen Sie eine andere Emailadresse.")
    return render_template("register.html", email = session.get("email"))

def profilEditieren():
    if session.get("email") is None:
        return redirect ("/")
    user = UserModel.find_by_email(session.get("email"))
    user.check_if_admin()
    isAdmin= user.ist_admin

    if request.method == "POST":
        password = request.form.get("password")
        if authenticate(user.email, password):
            password_new = request.form.get("new-password")
            if password_new and password_new == password:
                flash("Das neue Passwort darf nicht dasselbe wie das alte Passwort sein. Versuchen Sie es noch einmal.")
            else:
                vorname = request.form.get("vorname")
                nachname = request.form.get("nachname")
                geburtsdatum = request.form.get("geburtsdatum")
                if geburtsdatum:
                    geburtsdatum = geburtsdatum.replace("T", " ")
                user.vorname = vorname
                user.nachname = nachname
                user.geburtsdatum = geburtsdatum

                UserModel.save_to_db(user)
                flash("Profil erfolgreich editiert.")
        else:
            flash("Falsches Passwort. Versuchen Sie es noch einmal.")
    return render_template("profil.html", email=session.get("email"), isAdmin = isAdmin, user=user)

def ausloggen():
    session.clear()
    flash("Erfolgreich ausgeloggt.")
    return redirect("/")
