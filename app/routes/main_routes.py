import json
from typing import List, Optional

from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session, stream_with_context, \
    Response

from app.Response import ResponseInteractiveCTX
from app.assistant.actions.action import PrintAction
from app.assistant.intent import IntentTypes
from app.assistant.nlp.matcher import get_intent
from app.assistant.nlp.nlp_context import NLPContext
from app.config.app_vars import MAIN_MODEL, LOGGER, USER_LLM_CONVO_MAP, login_required, CRASH_USER_TEMPLATE, \
    RESPONSE_LLM_FORMATTING_TEMPLATE, APP_STATIC_CONFIG_DIR_FP, SESSION_CONTEXT_MAP, NPL_MODEL_CTX, PATTERNS_MAP
from app.llm.llm_conversation_ctx import LLMConversationCTX
from app.question import YesNoQuestion, InteractiveQuestion, MultipleChoiceQuestion
from app.session_ctx import SessionContext
from app.utils.llm_context_template_utils import apply_user_template

main_r = Blueprint('main_r', __name__)

PENDING_INTERACTIVE_MAP = {}


def __handle_intent(intent) -> Optional[ResponseInteractiveCTX]:
    interactive_ctx: ResponseInteractiveCTX = None
    question = None
    action_map = {}

    if intent == IntentTypes.GET_AGENT:
        interactive_ctx = ResponseInteractiveCTX(content="Do you want your agent to call you?",
                                                 response_type="question")
        question = YesNoQuestion(question_content=interactive_ctx.content)
        action_map = {"yes": PrintAction(action_args=[f"The user wants their agent to call them"]),
                   "no": PrintAction(action_args=[f"The user does not their agent to call them"])}


    elif intent == IntentTypes.GET_CLAIM:
        interactive_ctx = ResponseInteractiveCTX(content="Do you want to get a claim?",
                                                 response_type="question")
        question = YesNoQuestion(question_content=interactive_ctx.content)
        action_map = {"yes": PrintAction(action_args=[f"The user wants tyo get a claim"]),
                   "no": PrintAction(action_args=[f"The user does not want to get a claimm"])}

    elif intent == IntentTypes.FILE_CLAIM:
        interactive_ctx = ResponseInteractiveCTX(content="Do you want to file a claim?",
                                                 response_type="question")
        question = YesNoQuestion(question_content=interactive_ctx.content)
        action_map = {"yes": PrintAction(action_args=[f"The user wants file a claim"]),
                   "no": PrintAction(action_args=[f"The user does not want to file a claim"])}

    for k, v in action_map.items():
        question.register_choice(choice=k, action=v)

    interactive_ctx.interactive_question = question

    return interactive_ctx

@main_r.route('/')
@login_required
def index():
    return render_template('index.html')



@main_r.route('/answer', methods=['POST'])
@login_required
def answer_interactive():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    session_context: SessionContext = SESSION_CONTEXT_MAP.get(session["username"])

    data = request.get_json()
    question_id = data.get("question_id")
    answer = data.get("answer")

    if isinstance(answer, str):
        answer = answer.strip()
        answer = answer.lower()

    pending_interactives: List[InteractiveQuestion] = PENDING_INTERACTIVE_MAP.get(session_context.user_ctx.user_name)

    if not isinstance(pending_interactives, list):
        LOGGER.info(f"Interactive question {question_id} is not an interactive question for user {session_context.user_ctx.user_name}")
        return jsonify({"error": f"Interactive question {question_id} is not an interactive question for user {session_context.user_ctx.user_name}"}), 400

    if len(pending_interactives) == 0:
        LOGGER.info("No pending interactive questions")
        return jsonify({"error": "No pending interactive questions"}), 400

    has_pending = question_id in pending_interactives

    if not has_pending:
        LOGGER.info(f"No pending interactive questions with id {question_id}")
        return jsonify({"error": f"No pending interactive questions with id {question_id}"}), 400

    interactive_question: InteractiveQuestion = pending_interactives[pending_interactives.index(question_id)]

    if interactive_question is None:
        LOGGER.info(f"No pending interactive questions with id {question_id}")
        return jsonify({"error": f"No pending interactive questions with id {question_id}"}), 400

    interactive_question.submit_answer(answer)

    actions = []

    if isinstance(interactive_question, InteractiveQuestion) and not isinstance(interactive_question, MultipleChoiceQuestion):
        if interactive_question.get_actions() is not None:
            actions = interactive_question.get_actions()
            interactive_question.action.do_action(*interactive_question.action.action_args, **interactive_question.action.action_kwargs)
    elif isinstance(interactive_question, MultipleChoiceQuestion):
        actions = interactive_question.get_actions_from_choice(answer)

    for action in actions:
        action.do_action(*action.action_args, **action.action_kwargs)

    pending_interactives.remove(interactive_question)

    return jsonify({"status": 200})


@main_r.route('/chat', methods=['POST'])
@login_required
def chat():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    question = data.get('question')

    session_context: SessionContext = SESSION_CONTEXT_MAP.get(session["username"])

    if not question:
        return jsonify({'error': 'Missing question'}), 400

    nlp_ctx = NPL_MODEL_CTX
    doc = nlp_ctx(question)

    intent = get_intent(doc, PATTERNS_MAP, distance=1)

    convo: LLMConversationCTX = USER_LLM_CONVO_MAP.get(session['username'])

    if MAIN_MODEL is None:
        return jsonify({'error': 'LLM Model not found'}), 404

    context = apply_user_template(CRASH_USER_TEMPLATE, session["username"])

    with open(f"{APP_STATIC_CONFIG_DIR_FP}example-sf-policy.json", 'r') as f:
        context += "\n\n\nAnything to do with the customers policy, refer to their policy in JSON format: \n\n" + f.read()
    prompt = MAIN_MODEL.build_conversation_prompt(question, context, conversation_history=convo)

    example_question = YesNoQuestion(question_content=question)
    example_question = YesNoQuestion(question_content="Do you want you agent (Fred Kunnigham) to call you?")
    def generate():
        try:
            content = ""

            token_buffer = ""
            token_count = 0

            interactive_ctx = __handle_intent(intent)

            if isinstance(interactive_ctx, ResponseInteractiveCTX):
                yield f"data: {json.dumps(interactive_ctx.to_dict())}\n\n"
                interactive_questions = PENDING_INTERACTIVE_MAP.get(session_context.user_ctx.user_name)

                if not isinstance(interactive_questions, list):
                    interactive_questions = []
                    PENDING_INTERACTIVE_MAP.update({session_context.user_ctx.user_name: interactive_questions})

                interactive_questions.append(interactive_ctx.interactive_question)
                return

            # Wrap receive_chunk in a generator pattern
            for chunk in MAIN_MODEL.generate_response(prompt, logger=LOGGER):
                chunk = str(chunk)

                content += chunk
                latest_chunk = chunk
                token_count += len(chunk)
                token_buffer += chunk

                # LOGGER.debug(repr(chunk))
                if token_count > 10:
                    yield f"data: {json.dumps({'content': token_buffer, 'type': 'text'})}\n\n"
                    token_buffer = ''
                    token_count = 0

            yield f"data: {json.dumps({'content': token_buffer, 'type': 'text'})}\n\n"

            if len(content) == 0:
                LOGGER.warning(f"LLM gave blank response for question: '{question}'")
                return

            convo.add(question=question, response=content)
        except GeneratorExit:
            LOGGER.info(f"Generator exit for user {session['username']}")

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

