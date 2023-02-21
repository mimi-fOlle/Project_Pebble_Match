from flask import Blueprint

start = Blueprint("start", __name__)


@start.route('/start')