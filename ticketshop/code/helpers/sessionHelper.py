import datetime
from flask import Flask, session, render_template, request, redirect, flash
from models.userModel import UserModel

# auxiliary class which takes care of session related tasks
class SessionHelper:

    # checks whether person has user rights based on email stored in session
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

    # checks whether user has admin rights based on email stored in session
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

    # checks whether session stores an email
    @classmethod
    def user_check(cls, email):
        if email is None:
            return None
        user = UserModel.find_by_email(email)
        return user