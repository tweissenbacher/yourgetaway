import datetime

from flask import Flask, session, render_template, request, redirect, flash
from flask_restful import Api
from flask_jwt import JWT

from models.userModel import UserModel
class SessionHelper:

    @classmethod
    def admin_check(cls, session):
        if session.get("email") is None:
            return redirect ("/")

        user = UserModel.find_by_email(session.get("email"))
        user.check_if_admin()
        is_admin= user.is_admin
        if not is_admin:
            return redirect("/")