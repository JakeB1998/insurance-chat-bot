import logging
import os
from functools import wraps

from flask import redirect, session, url_for, request

from app.insurance_chatbot import ModelConfig, InsuranceLLM
from app.utils.llm_model_factory import create_model

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(module)s:%(lineno)d] %(message)s',
    handlers=[
        logging.StreamHandler()              # Also log to console
    ]
)

LOGGER = logging.getLogger(__name__)



APP_STATIC_CONFIG_DIR_FP = f"{os.getcwd()}{os.path.sep}app{os.path.sep}static{os.path.sep}config{os.path.sep}"

CRASH_CONTEXT_TEMPLATE = ""

__FP = f"{APP_STATIC_CONFIG_DIR_FP}crash-context-template.txt"

try:
    if os.path.isfile(__FP):
        with open(__FP, "r", encoding="utf-8") as f:
            CRASH_CONTEXT_TEMPLATE = f.read()

    else:
        LOGGER.warning(f"File {__FP} not found.")
except Exception as e:
    LOGGER.error(f"Failed to load context from {__FP}", e)

del __FP

MAIN_MODEL = create_model()
MAIN_MODEL.load_model()

USER_MODEL_MAP = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login_r.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
