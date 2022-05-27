import json
import os
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from .. import db
from ..model import Section, Line, User

# from random import randrange
# from lorem_text import lorem


index = Blueprint("index", __name__)


@index.route("/", methods=["GET"])
def index_view():
    lines = Line.query.all()
    return render_template("index.html", user=current_user, lines=lines)

