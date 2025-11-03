import logging
import uuid
from typing import List, Any, Dict

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


    def __str__(self):
        return self.question_content


class InteractiveQuestion(Question):
    def __init__(self, question_content: str, question_type: str = QuestionTypes.INTERACTIVE, answered: bool = False, answer: Any = None, action: Action = None):
        super().__init__(question_content=question_content, question_type=question_type, answered=answered, answer=answer)
        self.choice_action_map = {}
        self.__action: Action = action


    def get_actions(self) -> List[Action]:
        return [self.__action] if self.__action is not None else None


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
    def __init__(self, question_content: str, choices: List[str],  question_type: str = QuestionTypes.MULTI_CHOICE, answered: bool = False, answer: Any = None, action: Action = None, logger = None):
        super().__init__(question_content=question_content, question_type=question_type, answered=answered, action = action)
        self.choices = choices
        self.choice_action_map: Dict[str, List[Action]] = {}
        self.__logger = logger if logger else logging.getLogger(__name__)

        if not isinstance(self.choices, list):
            raise TypeError("Choices must be a list")


    def get_actions(self) -> List[Action]:
        return self.choice_action_map.values() if self.choice_action_map is not None else None


    def get_actions_from_choice(self, choice):
        if isinstance(self.choice_action_map, dict):
            if choice in self.choice_action_map:
                return [self.choice_action_map[choice]]
        return None

    def register_choice(self, choice, action = None):
        if choice is None:
            raise ValueError("Choice cannot be None")

        if choice not in self.choices:
            self.choice_action_map[choice] = []

        self.choice_action_map.update({choice: action})

    def register_action(self, choice, action, add_choice: bool = False, logger = None):
        if logger is None:
            logger = self.__logger

        if choice not in self.choices:
            if not add_choice:
                logger.warning(f"Cannot add action for choice {str(choice)} as it is not registered")
                return False

        self.choice_action_map.update({choice: action})

        return True

    def to_dict(self):
        ret = super().to_dict()
        ret.update({"choices": self.choices})
        return ret

    def __str__(self):
        return str(self.to_dict())


class YesNoQuestion(MultipleChoiceQuestion):
    def __init__(self, question_content: str, question_type: str = QuestionTypes.YES_NO, answered: bool = False, answer: Any = None, action: Action = None):
        super().__init__(question_content=question_content, question_type=question_type,  choices=["yes", "no"], answered=answered, answer=answer, action=action)


    def __str__(self):
        return super().__str__()