import datetime

from flask import Flask, session, render_template, request, redirect, flash
from flask_restful import Api
from flask_jwt import JWT

from models.userModel import UserModel
class SessionHelper:

    @classmethod
    def normal_user_check(cls, email):
        user = SessionHelper.user_check(email)
        if user is None:
            return None
        user.check_if_admin()
        is_admin = user.is_admin
        if is_admin:
            return None
        return user

    @classmethod
    def admin_check(cls, email):
        user = SessionHelper.user_check(email)
        if user is None:
            return None
        user.check_if_admin()
        is_admin = user.is_admin
        if is_admin:
            return user
        return None

    @classmethod
    def user_check(cls, email):
        if email is None:
            return None
        user = UserModel.find_by_email(email)
        return user