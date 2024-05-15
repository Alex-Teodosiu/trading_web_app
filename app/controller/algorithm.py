import functools
import requests

from flask import (
    Blueprint,
    render_template
)


bp = Blueprint('algorithm', __name__, url_prefix='/algorithm')

@bp.route('/')
def algorithm():
    return render_template('/home/algorithms.html')