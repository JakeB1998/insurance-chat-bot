

from flask import Blueprint, jsonify, render_template, request

from app.config.app_vars import MODEL, LOGGER

main_r = Blueprint('main_r', __name__)


@main_r.route('/')
def index():
    return render_template('index.html')


@main_r.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    # Extract 'question' and 'context' keys safely
    question = data.get('question')
    context = data.get('context', '')

    if not question:
        return jsonify({'error': 'Missing question or context'}), 400

    prompt = MODEL.build_conversation_prompt(question, context)
    response, tokens, elapsed_time = MODEL.generate_response(prompt, logger=LOGGER)

    # Add to conversation history
    MODEL.conversation_history.append({
        "user": question,
        "assistant": response
    })



    # Do something with question and context
    return jsonify({
        'received_question': question,
        'received_context': context,
        'response': response
    })

