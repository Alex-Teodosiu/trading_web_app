import functools
import requests

from flask import (
    Blueprint,
    render_template
)


bp = Blueprint('tradingaccount', __name__, url_prefix='/traddingaccount')

@bp.route('/')
def tradingaccount():
    return render_template('/home/tradingaccount.html')