from app.insurance_chatbot import InsuranceLLM, ModelConfig


def create_model_for_user(username, context: str = None):
    config = ModelConfig()




    model = InsuranceLLM(config, system_context=context)

    return model



def create_model():
    config = ModelConfig()
    model = InsuranceLLM(config, system_context="")
    return model
