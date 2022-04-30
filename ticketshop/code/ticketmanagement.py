import datetime

from flask import Flask, session, render_template, request, redirect, flash



# @app.route("/tickets/neu", methods =["GET", "POST"])
# def ticket_anlegen():
#     if session.get("email") is None:
#         return redirect ("/")
#     return render_template("ticketAnlegen.html", email=session.get("email"))

def ticket_anlegen():
    if session.get("email") is None:
        return redirect ("/")
    return render_template("ticketAnlegen.html", email=session.get("email"))