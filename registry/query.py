from typing import Dict, Any, Tuple, List
from .model import AgentInfo
from runtime.state import SharedState

class QueryAgent:
    def __init__(self) -> None:
        pass
        
    def find_by_model(self, model: str) -> Tuple[str, Dict[str, AgentInfo]]:
        """
        
        """
        for i, v in SharedState.agents.items():
            current_model = v.mod.model
            
            if model == current_model:
                return i, v
            
            continue
        
        return None
    
    def find_by_provider(self, provider: str) -> Tuple[str, List[dict] | Dict[str, AgentInfo]]:
        """
        
        """
        model_provider: List[Dict[str, AgentInfo]] = []
        
        for i, v in SharedState.agents.items():
            current_provider = v.provider
            
            if provider == current_provider:
                model_provider.append[{i: v}]
            
            continue
        
        if not model_provider:
            return None
        elif len(model_provider) < 1:
            return model_provider[0]
        else:
            return model_provider