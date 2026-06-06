from src.core.llm import LLM
from abc import ABC, abstractmethod
from typing import Optional

class Agent(ABC):
    def __init__(
        self, 
        llm: LLM,
        system_prompt: Optional[str] = None,
    ):
        self.llm = llm
        self.system_prompt = system_prompt
        self.history = []

    @abstractmethod
    def run(self):
        pass

    def add_message(self, message):
        self.history.append(message)
    
    def clear_history(self):
        self.history = []
    
    def get_history(self):
        return self.history.copy()