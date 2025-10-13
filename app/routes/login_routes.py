

from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from app.config.app_vars import MAIN_MODEL, LOGGER, CRASH_CONTEXT_TEMPLATE, USER_MODEL_MAP
from app.utils.llm_model_factory import create_model_for_user

login_r = Blueprint('login_r', __name__)




@login_r.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            model = create_model_for_user(username=username, context_template=CRASH_CONTEXT_TEMPLATE)
            model.load_model()
            USER_MODEL_MAP.update({username:  model}),

            return redirect(url_for('main_r.index', username=username))
        else:
            return render_template('login.html', error="Username is required.")

    return render_template('login.html')




@login_r.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_r.login'))