
from app.question import InteractiveQuestion



class ResponseInteractiveCTX():
    def __init__(self, content: str, response_type: str, interactive_question: InteractiveQuestion = None):
        self.content = content
        self.response_type = response_type
        self.interactive_question: InteractiveQuestion = interactive_question

    def to_dict(self):
        ret = {"content": self.content, "type": self.response_type}
        ret.update(self.interactive_question.to_dict())
        return ret