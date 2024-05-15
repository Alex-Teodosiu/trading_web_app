import functools
import requests

from flask import (
    Blueprint,
    render_template
)


bp = Blueprint('market', __name__, url_prefix='/market')

@bp.route('/viewstocks')
def viewstocks():
    return render_template('/home/viewstocks.html')