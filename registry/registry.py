"""
***
Structure of agents.json

{
    "name": "it's name model, not the model",
    "provider": "provider who published or built the model",
    "vendor": "who published the model",
    "uuid": "registry code for trust input",
    "mod": {
        "model": "the model",
        "description": "description about the model",
        
        "is_key": {
            "status": bool,
            "key": "the key",
            "protection": bool,
        },
        
        "is_api": {
            "status": bool,
            "headers": "if is api",
            "endpoint": "endpoint",
        },
    }
}

***
"""

import json
from .model import (METADATA_FILE, AgentInfo, IdentityModel, IsKey, IsApi, asdict)
from ..runtime.state import SharedState

def load() -> bool:
    data = {}
    agent_data = {}
    
    with open(METADATA_FILE, "r") as f:
        data = json.load(f)
        
    for i, v in data.items():
        
        AI = AgentInfo(
            name=v["name"],
            provider=v["provider"],
            vendor=v["vendor"],
            uuid=v["uuid"],
            
            mod=IdentityModel(
                model=v["mod"]["model"],
                description=v["mod"]["description"],
                
                is_key=IsKey(**v["mod"]["is_key"]),
                is_api=IsApi(**v["mod"]["is_api"])
            )
        )
        
        agent_data[i] = AI
        
    SharedState.agents = agent_data

# Registry Layer
class RegistryModel:
    def __init__(self):
        pass
    
    def save(self) -> None:
        """
        
        """
        data = {}
        for i, v in SharedState.agents.items():
            data[i] = asdict(obj=v)
        
        with open(METADATA_FILE, "w") as f:
            json.dump(
                obj=data,
                fp=f,
                indent=4
            )
            
            del data
    
    def insert(self, agent: AgentInfo):
        import uuid
        
        agent.uuid = str(uuid.uuid4())
        SharedState.agents[agent.uuid] = agent
        self.save()
        
        return True
    
    def read(self) -> dict:
        return SharedState.agents
    
    def update(self, identify_id: str, agent: AgentInfo):
        if not identify_id in SharedState.agents:
            return False
        
        SharedState.agents[identify_id] = agent
        self.save()
    
    def delete(self, identify_id: str):
        if not identify_id in SharedState.agents:
            return True
        
        del SharedState.agents[identify_id]
        self.save()
        
        return True
