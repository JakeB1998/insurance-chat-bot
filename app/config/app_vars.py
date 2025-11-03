import json
import logging
import os
from functools import wraps

from flask import redirect, session, url_for, request

from app.assistant.nlp.nlp_config import NLPConfig
from app.assistant.nlp.nlp_context import NLPContext
from app.llm.llm_config import ModelConfig
from app.llm.llm_model_factory import create_model
from app.session_ctx import SessionContext
from app.user_context import UserContext
from app.utils.file_utils import load_from_file

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [Thread:%(thread)d] [%(levelname)s] [%(module)s:%(lineno)d] %(message)s',
    handlers=[
        logging.StreamHandler()              # Also log to console
    ]
)

LOGGER = logging.getLogger(__name__)


APP_STATIC_CONFIG_DIR_FP = f"{os.getcwd()}{os.path.sep}app{os.path.sep}static{os.path.sep}config{os.path.sep}"

LLM_SYSTEM_CTX_MSG = load_from_file(f"{APP_STATIC_CONFIG_DIR_FP}general-context.txt")
LLM_CRASH_SYSTEM_CTX_MSG = load_from_file(f"{APP_STATIC_CONFIG_DIR_FP}crash-context.txt")
CRASH_USER_TEMPLATE = load_from_file(f"{APP_STATIC_CONFIG_DIR_FP}crash-user-context-template.txt")
RESPONSE_LLM_FORMATTING_TEMPLATE = load_from_file(f"{APP_STATIC_CONFIG_DIR_FP}response-formatting-template.txt")

# CRASH_SYSTEM_CTX += "\n\n" + RESPONSE_LLM_FORMATTING_TEMPLATE

USER_LLM_CONVO_MAP = {}
SESSION_CONTEXT_MAP = {}

with open(f"{APP_STATIC_CONFIG_DIR_FP}nlp{os.path.sep}nlp-patterns-config.json", "r") as fp:
    PATTERNS_MAP = json.load(fp)



NPL_MODEL_CTX = NLPContext(nlp_config=NLPConfig(model_name="nlp", language="en", processors=['tokenize','mwt','pos','lemma','depparse']))
# MAIN_MODEL = create_model(system_context=CRASH_SYSTEM_CTX, config=ModelConfig(model_name="Qwen2.5-3B-IQ3_M", model_file="Qwen2.5-3B-IQ3_M.gguf"))
GEN_AI_MODEL_CTX = create_model(system_context=LLM_SYSTEM_CTX_MSG, config=ModelConfig())
GEN_AI_MODEL_CTX.load_model()



