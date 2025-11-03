from typing import List, Union

import os
from pathlib import Path

from llama_cpp import Llama

from app.llm.llm_conversation_ctx import LLMConversationCTX


def load_model(
    model_file_path: str,
    n_gpu_layers: int,
    n_ctx: int,
    n_batch: int,
    num_beams: int,
    verbose: bool,
    use_mlock: bool,
    use_mmap: bool,
    offload_kqv: bool
) -> Llama:
    try:
        llm_ctx = Llama(
            model_path=model_file_path,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
            n_batch=n_batch,
            num_beams=num_beams,
            verbose=verbose,
            use_mlock=use_mlock,
            use_mmap=use_mmap,
            offload_kqv=offload_kqv
        )
        return llm_ctx

    except Exception as e:
        raise e

def build_prompt(question: str, system_context: str, context: str = "", conversation_history: Union[List[dict], LLMConversationCTX] = None) -> str:
    if not context:
        context = ""

    if conversation_history is None:
        conversation_history = []

    if isinstance(conversation_history, LLMConversationCTX):
        conversation_history = conversation_history.conversation_history

    prompt = f"System: {system_context}\n\n"

    # Add conversation history
    for exchange in conversation_history:
        prompt += f"User: {exchange['user']}\n\n"
        prompt += f"Assistant: {exchange['assistant']}\n\n"

    # Add the new question
    if context:
        prompt += f"User: Context: {context}\nQuestion: {question}\n\n"
    else:
        prompt += f"User: {question}\n\n"

    prompt += "Assistant:"

    return prompt



# def build_prompt(question: str, system_context: str, context: str = "", conversation_history: Union[List[dict], LLMConversationCTX] = None) -> str:
#     if not context:
#         context = ""
#
#     if conversation_history is None:
#         conversation_history = []
#
#     if isinstance(conversation_history, LLMConversationCTX):
#         conversation_history = conversation_history.conversation_history
#
#     prompt = f"==== SYSTEM INSTRUCTIONS ====\n {system_context}\n"
#
#     # Add conversation history
#     if len(conversation_history) > 0:
#         prompt+= "==== CONVERSATION_HISTORY ====\n"
#
#     for exchange in conversation_history:
#         prompt += f"User: {exchange['user']}\n"
#         prompt += f"Assistant: {exchange['assistant']}\n"
#
#     # Add the new question
#     if context:
#         prompt += f"==== CONTEXT ====\n {context}\n"
#
#     prompt += f"==== USER INPUT ====\n {question}\n"
#
#
#     prompt += "==== ASSISTANT ====\n"
#
#
#     return prompt