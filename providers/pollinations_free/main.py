from typing import Tuple
from contracts.agents import AgentBaseModel
from requests import Session

class pollinations(AgentBaseModel):
    def __init__(self) -> None:
        super().__init__()
        self._session = Session()
        
    def agent(self, prompt: str) -> Tuple[bool, str]:
        """
        
        """
        
        response = self._session.get(f"https://image.pollinations.ai/prompt/{prompt}")
        return self._image.save({"part": response})