

from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session

from app.config.app_vars import MAIN_MODEL, LOGGER, USER_LLM_CONVO_MAP, login_required
from app.llm.llm_conversation_ctx import LLMConversationCTX

main_r = Blueprint('main_r', __name__)



@main_r.route('/')
@login_required
def index():
    return render_template('index.html')



@main_r.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()

    # Extract 'question' and 'context' keys safely
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Missing question or context'}), 400

    convo: LLMConversationCTX = USER_LLM_CONVO_MAP.get(session['username'])

    if MAIN_MODEL is None:
        return jsonify({'error': 'LLM Model not found'}), 404

    def receive_chunk(chunk):
        pass

    context = f"The customers name is {session['username']}. They were in a car accident. give them a step by step guide on what to do starting with step 1."
    prompt = MAIN_MODEL.build_conversation_prompt(question, f"The users name is {session['username']}", conversation_history=convo)
    response, tokens, elapsed_time = MAIN_MODEL.generate_response(prompt, logger=LOGGER, chunk_callback=receive_chunk)

    convo.add(question=question, response=response)



    # Do something with question and context
    return jsonify({
        'received_question': question,
        'response': response
    })

