from typing import List, Any, Tuple
from core import ProviderManager

class Imagine:
    def __init__(self) -> None:
        self._trust_worker: ProviderManager = ProviderManager()
        
    def _handler_prompt(self, prompt: str | List[str]) -> str:
        """
        
        """
        def do_run(prompt: str) -> Tuple[int, str, Any]:
            return self._trust_worker.run_worker(prompt=prompt)
        
        if isinstance(prompt, str):
            return do_run(prompt=prompt)
        
        elif isinstance(prompt, List[str]):
            responses = []
            for c in prompt:
                responses.append(do_run(prompt=c))
                
            return responses
            
    
    def generate(self, prompt: str | List[str]) -> str:
        """
        
        """
        
        if not prompt:
            return ValueError("'prompt' must be string, not None.")
        
        response = self._handler_prompt(prompt=prompt)
        
        if not response:
            return "No Response Here"
        
        if isinstance(response, dict):
            if response["at"] and response["worker"]:
                return response["response"]
            
        elif isinstance(response, List[dict]):
            responses = []
            for object in response:
                if object["at"] and object["worker"]:
                    responses.append(object["response"])
                    
            return object