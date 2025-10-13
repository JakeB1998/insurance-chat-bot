

from flask import Blueprint, render_template, request, redirect, url_for, session
from app.config.app_vars import CRASH_SYSTEM_CTX, USER_LLM_CONVO_MAP
from app.llm.llm_conversation_ctx import LLMConversationCTX
from app.llm.llm_model_factory import create_model

login_r = Blueprint('login_r', __name__)




@login_r.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            USER_LLM_CONVO_MAP.update({username:  LLMConversationCTX()}),

            return redirect(url_for('main_r.index'))
        else:
            return render_template('login.html', error="Username is required.")

    return render_template('login.html')




@login_r.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_r.login'))