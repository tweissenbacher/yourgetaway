import json
import os
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
import requests

from website.model.line import LineSection
from .. import db
from ..model import Section, Line, Trip, Route


trips = Blueprint("trips", __name__)


@trips.route("/trips/", methods=["GET", "POST"])
@login_required
def lines_view():
    trips = Trip.query.all()
    return render_template("lines.html", user=current_user, trips=trips)

