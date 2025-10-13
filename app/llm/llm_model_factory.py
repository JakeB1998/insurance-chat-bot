from app.llm.insurance_chatbot import InsuranceLLM, ModelConfig



def create_model(system_context = ""):
    config = ModelConfig()
    model = InsuranceLLM(config, system_context=system_context)
    return model
