import logging
import os
from functools import wraps

from flask import redirect, session, url_for, request

from app.llm.llm_config import ModelConfig
from app.llm.llm_model_factory import create_model
from app.utils.file_utils import load_from_file

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(module)s:%(lineno)d] %(message)s',
    handlers=[
        logging.StreamHandler()              # Also log to console
    ]
)

LOGGER = logging.getLogger(__name__)



APP_STATIC_CONFIG_DIR_FP = f"{os.getcwd()}{os.path.sep}app{os.path.sep}static{os.path.sep}config{os.path.sep}"

CRASH_SYSTEM_CTX = load_from_file(f"{APP_STATIC_CONFIG_DIR_FP}crash-context.txt")
CRASH_USER_TEMPLATE = load_from_file(f"{APP_STATIC_CONFIG_DIR_FP}crash-user-context-template.txt")
RESPONSE_LLM_FORMATTING_TEMPLATE = load_from_file(f"{APP_STATIC_CONFIG_DIR_FP}response-formatting-template.txt")

# CRASH_SYSTEM_CTX += "\n\n" + RESPONSE_LLM_FORMATTING_TEMPLATE

MAIN_MODEL = create_model(system_context=CRASH_SYSTEM_CTX, config=ModelConfig())
MAIN_MODEL.load_model()

USER_LLM_CONVO_MAP = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login_r.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
