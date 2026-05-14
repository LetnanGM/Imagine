from typing import Dict
from registry.model import AgentInfo

class SharedState:
    cached: dict = {}
    agents: Dict[str, AgentInfo] = {}
    
    loaded: bool = False
    