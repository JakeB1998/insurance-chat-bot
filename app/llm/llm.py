# Attached under `Files and Versions` (inference_open-insurance-llm-gguf.py)
import logging
import os
import time
from pathlib import Path
from llama_cpp import Llama
from rich.console import Console
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Union

from app.llm.llm_config import ModelConfig
from app.llm.llm_conversation_ctx import LLMConversationCTX
from app.utils.llm_utils import build_conversation_prompt, load_model


class InsuranceLLMCTX:
    def __init__(self, config: ModelConfig, system_context: str =""):
        self.config = config
        self.llm_ctx = None

        self.system_context = system_context


    def load_model(self) -> None:

        quantized_path = os.path.join(os.getcwd(), "gguf_dir")
        directory = Path(quantized_path)
        try:
            model_path = str(list(directory.glob(self.config.model_file))[0])
        except IndexError as e:
            raise e

        self.llm_ctx = load_model(
            model_file_path=model_path,
            n_gpu_layers=self.config.n_gpu_layers,
            n_ctx=self.config.n_ctx,
            n_batch=self.config.n_batch,
            num_beams=self.config.num_beams,
            verbose=self.config.verbose,
            use_mlock=self.config.use_mlock,
            use_mmap=self.config.use_mmap,
            offload_kqv=self.config.offload_kqv
        )

    def build_conversation_prompt(self, new_question: str, context: str = "", conversation_history: Union[List[dict], LLMConversationCTX] = None) -> str:
        if conversation_history is None:
            conversation_history = []

        return build_conversation_prompt(question=new_question, system_context=self.system_context, context=context, conversation_history=conversation_history)

    def generate_response(self, prompt: str, logger = None):
        if logger is None:
            logger = logging.getLogger(__name__)

        if not self.llm_ctx:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        complete_response = ""
        token_count = 0
        start_time = time.time()

        try:
            for chunk in self.llm_ctx.create_completion(
                prompt,
                max_tokens=self.config.max_tokens,
                top_k=self.config.top_k,
                top_p=self.config.top_p,
                temperature=self.config.temperature,
                repeat_penalty=self.config.repeat_penalty,
                stream=True
            ):
                text_chunk = chunk["choices"][0]["text"]
                complete_response += text_chunk
                token_count += 1
                yield text_chunk

        except Exception as e:
            logger.error(f"\n[red]Error generating response: {str(e)}[/red]")
            return f"I encountered an error while generating a response. Please try again or ask a different question.", 0, 0


