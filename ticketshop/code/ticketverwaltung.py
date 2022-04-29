import datetime

from flask import Flask, session, render_template, request, redirect, flash



#Tickets

@app.route("/tickets/neu", methods =["GET", "POST"])
def ticketAnlegen():
    if session.get("email") is None:
        return redirect ("/")
    return render_template("ticketAnlegen.html", email=session.get("email"))