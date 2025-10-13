

from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session, stream_with_context, \
    Response

from app.config.app_vars import MAIN_MODEL, LOGGER, USER_LLM_CONVO_MAP, login_required, CRASH_USER_TEMPLATE, \
    RESPONSE_LLM_FORMATTING_TEMPLATE, APP_STATIC_CONFIG_DIR_FP
from app.llm.llm_conversation_ctx import LLMConversationCTX
from app.utils.llm_context_template_utils import apply_user_template

main_r = Blueprint('main_r', __name__)



@main_r.route('/')
@login_required
def index():
    return render_template('index.html')



@main_r.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Missing question'}), 400

    convo: LLMConversationCTX = USER_LLM_CONVO_MAP.get(session['username'])

    if MAIN_MODEL is None:
        return jsonify({'error': 'LLM Model not found'}), 404

    context = apply_user_template(CRASH_USER_TEMPLATE, session["username"])

    with open(f"{APP_STATIC_CONFIG_DIR_FP}example-sf-policy.json", 'r') as f:
        context += "\n\n\nAnything to do with the customers policy, refer to their policy in JSON format: \n\n" + f.read()
    prompt = MAIN_MODEL.build_conversation_prompt(question, context, conversation_history=convo)

    def generate():
        response_accum = ""
        latest_chunk = ""
        token_buffer = ""
        token_count = 0
        # Wrap receive_chunk in a generator pattern
        for chunk in MAIN_MODEL.generate_response(prompt, logger=LOGGER):
            chunk = str(chunk)
            response_accum += chunk
            token_count += len(chunk)
            token_buffer += chunk

            # LOGGER.debug(repr(chunk))
            if token_count > 10:
                yield f"data: {token_buffer}\n\n"
                token_buffer = ''
                token_count = 0

        yield f"data: {token_buffer}\n\n"

        convo.add(question=question, response=response_accum)

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

