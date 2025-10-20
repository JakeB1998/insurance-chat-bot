import uuid
from typing import List, Any

class QuestionTypes:
    DEFAULT = "DEFAULT"
    MULTI_CHOICE = "MULTI_CHOICE"
    INTERACTIVE = "INTERACTIVE"
    YES_NO = "YES_NO"

class Question:
    def __init__(self, question_content: str, question_type: str, answered: bool = False, answer: Any = None):
        self.id = str(uuid.uuid4())
        self.question_content = question_content
        self.question_type = question_type
        self.answered = answered
        self.answer = answer


    def answer(self, answer: Any, answered: bool = True):
        self.answer = answer
        self.answered = answered


class InteractiveQuestion(Question):
    def __init__(self, question_content: str, question_type: str = QuestionTypes.INTERACTIVE, answered: bool = False, answer: Any = None):
        super().__init__(question_content=question_content, question_type=question_type, answered=answered, answer=answer)

    def to_dict(self):
        return {
            "question_id": self.id,
            "content": self.question_content,
        }


class MultipleChoiceQuestion(InteractiveQuestion):
    def __init__(self, question_content: str, choices: List[str],  question_type: str = QuestionTypes.MULTI_CHOICE, answered: bool = False, answer: Any = None):
        super().__init__(question_content=question_content, question_type=question_type, answered=answered)
        self.choices = choices

    def to_dict(self):
        ret = super().to_dict()
        ret.update({"choices": self.choices})
        return ret


class YesNoQuestion(MultipleChoiceQuestion):
    def __init__(self, question_content: str, question_type: str = QuestionTypes.YES_NO, answered: bool = False, answer: Any = None):
        super().__init__(question_content=question_content, question_type=question_type,  choices=["yes", "no"], answered=answered, answer=answer)