from app.insurance_chatbot import InsuranceLLM, ModelConfig


def create_model_for_user(username, context_template: str = None):
    config = ModelConfig()

    context = ""

    if context_template is not None:
        context = context_template
        context = context.replace("{name}", username)


    model = InsuranceLLM(config, context=context)

    return model



def create_model():
    config = ModelConfig()
    model = InsuranceLLM(config, context="")
    return model
