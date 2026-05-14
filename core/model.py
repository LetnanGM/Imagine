from pydantic import BaseModel, field_validator
from typing import Dict, Any, Callable, Type
import bleach

class SetImagine:
    outfile: str = "./output/"

class ModelData:
    vendor : str
    company : str
    provider : str
    title : str
    uuid_register : str
    
    is_api : bool
    request_header : Dict[str, Any] = None
    instance_request : Callable | Type
    endpoint : str
    api_key : str

class ImageMetadata(BaseModel):
    name : str
    prompt : str
    description : str
    author : str
    model : str
    trust : int
    
    @field_validator("trust")
    def trust_level(trust: int) -> int:
        trust_level = [0, 1]
        if trust not in trust_level:
            return 0
        
        return trust
    
    @field_validator("name")
    def name(name) -> str:
        return bleach.clean(name)
            
    @field_validator("prompt")
    def prompt(prompt) -> str:
        return bleach.clean(prompt)
        
    @field_validator("description")
    def desc(description_text: str) -> str:
        return bleach.clean(description_text)
        
    @field_validator("author")
    def author(name: str) -> str:
        return bleach.clean(name)
        
    @field_validator("model")
    def model(name_model: str) -> str:
        return bleach.clean(name_model)
    