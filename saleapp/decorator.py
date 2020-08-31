from flask import session, redirect, url_for, request
from functools import wraps
from flask_login import current_user


def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("signin_user", next=request.url))

        return f(*args, **kwargs)

    return check
