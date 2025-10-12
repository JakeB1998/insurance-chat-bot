import logging

from insurance_chat import ModelConfig, InsuranceLLM


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(module)s:%(lineno)d] %(message)s',
    handlers=[
        logging.StreamHandler()              # Also log to console
    ]
)

LOGGER = logging.getLogger(__name__)

config = ModelConfig()
MODEL = InsuranceLLM(config)
MODEL.load_model()