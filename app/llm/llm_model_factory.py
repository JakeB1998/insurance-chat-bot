from app.llm.llm import InsuranceLLMCTX, ModelConfig



def create_model(system_context = ""):
    config = ModelConfig()
    model = InsuranceLLMCTX(config, system_context=system_context)
    return model
