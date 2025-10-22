import uuid
from typing import List, Any

from app.assistant.actions.action import Action


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


    def submit_answer(self, answer: Any, answered: bool = True):
        self.answer = answer
        self.answered = answered


class InteractiveQuestion(Question):
    def __init__(self, question_content: str, question_type: str = QuestionTypes.INTERACTIVE, answered: bool = False, answer: Any = None, action: Action = None):
        super().__init__(question_content=question_content, question_type=question_type, answered=answered, answer=answer)
        self.action: Action = action

    def to_dict(self):
        return {
            "question_id": self.id,
            "content": self.question_content,
        }

    def __contains__(self, item):
        if isinstance(item, Question):
            return self.__eq__(item)

        if isinstance(item, str):
            item = item.lower()

        return item == super().id

    def __eq__(self, other):
        if isinstance(other, Question):
            return self.id == other.id

        if isinstance(other, str):
            other = other.lower()
            return self.id == other

        return super().__eq__(other)



class MultipleChoiceQuestion(InteractiveQuestion):
    def __init__(self, question_content: str, choices: List[str],  question_type: str = QuestionTypes.MULTI_CHOICE, answered: bool = False, answer: Any = None, action: Action = None):
        super().__init__(question_content=question_content, question_type=question_type, answered=answered, action = action)
        self.choices = choices

    def to_dict(self):
        ret = super().to_dict()
        ret.update({"choices": self.choices})
        return ret


class YesNoQuestion(MultipleChoiceQuestion):
    def __init__(self, question_content: str, question_type: str = QuestionTypes.YES_NO, answered: bool = False, answer: Any = None, action: Action = None):
        super().__init__(question_content=question_content, question_type=question_type,  choices=["yes", "no"], answered=answered, answer=answer, action=action)