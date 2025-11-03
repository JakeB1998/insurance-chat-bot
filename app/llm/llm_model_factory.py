from app.llm.llm import InsuranceLLMCTX, ModelConfig



def create_model(system_context = "", config: ModelConfig = None) -> InsuranceLLMCTX:
    config = ModelConfig() if config is None else config
    model = InsuranceLLMCTX(config, system_context=system_context)
    return model
