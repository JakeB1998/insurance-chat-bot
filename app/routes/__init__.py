from functools import wraps

from flask import redirect, session, url_for, request

from app.config.app_vars import SESSION_CONTEXT_MAP
from app.session_ctx import SessionContext
from app.user_context import UserContext


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login_r.login', next=request.url))

        if not SESSION_CONTEXT_MAP.get(session['username']):
            SESSION_CONTEXT_MAP.update({session['username']: SessionContext(user_ctx=UserContext(user_name=session['username']))})
        return f(*args, **kwargs)
    return decorated_function