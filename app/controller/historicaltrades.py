import functools
import requests

from flask import (
    Blueprint,
    render_template
)


bp = Blueprint('historicaltrades', __name__, url_prefix='/historicaltrades')

@bp.route('/')
def historicaltrades():
    return render_template('/home/historicaltrades.html')