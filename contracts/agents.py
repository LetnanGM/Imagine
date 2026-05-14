from typing import Tuple
from abc import ABC, abstractmethod

class AgentBaseModel(ABC):
    __identify__ = "CODE-REGISTRY like from agent.py"
    
    def __init__(self) -> None:
        from core import Image
        self._image = Image()
    
    @abstractmethod
    def agent(self, prompt: str) -> Tuple[bool, str]:
        raise NotImplementedError("currently not implemented")
    