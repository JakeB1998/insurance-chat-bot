

from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session

from app.config.app_vars import MAIN_MODEL, LOGGER, USER_MODEL_MAP, login_required

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
    context = data.get('context', '')

    if not question:
        return jsonify({'error': 'Missing question or context'}), 400

    model = USER_MODEL_MAP.get(session['username'])

    if model is None:
        return jsonify({'error': 'LLM Model not found'}), 404

    prompt = model.build_conversation_prompt(question, context)
    response, tokens, elapsed_time = model.generate_response(prompt, logger=LOGGER)

    # Add to conversation history
    model.conversation_history.append({
        "user": question,
        "assistant": response
    })



    # Do something with question and context
    return jsonify({
        'received_question': question,
        'received_context': context,
        'response': response
    })

