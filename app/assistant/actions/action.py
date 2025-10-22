import logging
import uuid
from abc import abstractmethod
from typing import List, Dict, Any


class Action:
    def __init__(self, action_id: str = None, name: str = None, action_args: List[Any] = None, action_kwargs: Dict[str, Any] = None):
        self.action_id = action_id
        self.name = name
        self.action_args = action_args
        self.action_kwargs = action_kwargs


        if self.action_id is None:
            self.action_id = str(uuid.uuid4())

        if self.action_args is None:
            self.action_args = []

        if self.action_kwargs is None:
            self.action_kwargs = {}

    @abstractmethod
    def do_action(self):
        pass

class PrintAction(Action):
    def __init__(self, action_id: str = None, name: str = None, action_args: List[str] = None, action_kwargs: Dict[str, Any] = None, logger = None):
        super().__init__(action_id=action_id, name=name, action_args=action_args, action_kwargs=action_kwargs)
        self.logger = logger

        if self.logger is None:
            self.logger = logging.getLogger(__name__)

    def do_action(self, *args, **kwargs):
        self.logger.info(f"Printing action {self.action_id}. args: {args}, kwargs: {kwargs}")

