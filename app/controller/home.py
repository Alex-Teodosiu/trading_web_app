import functools
import requests

from flask import (
    Blueprint,
    render_template
)


bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/')
def home_page():
    return render_template('/home/home.html')
