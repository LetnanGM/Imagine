from dataclasses import dataclass, asdict

METADATA_FILE = "agents.json"

# Model Layer 
@dataclass
class IsKey:
    status : bool
    key : str | bytes
    protection : str

@dataclass
class IsApi:
    status : bool
    headers : dict
    endpoint : str

@dataclass
class IdentityModel:
    model : str
    description : str
    is_key : IsKey
    is_api : IsApi

@dataclass
class AgentInfo:
    name : str
    provider : str
    vendor : str
    uuid : str
    mod : IdentityModel
