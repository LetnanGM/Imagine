from typing import Dict, List, Tuple, Any
from contracts.agents import AgentBaseModel
from runtime.state import SharedState

import inspect

class localState:
    is_loaded: bool = False

class ScanWorker:
    def __init__(self) -> None:
        pass
    
    def filter_worker(self, module) -> None:
        for name, obj in inspect.getmembers(module, inspect.isclass):
            
            if not isinstance(obj, type):
                continue
            
            # skip imported class
            if obj.__module__ != module.__name__:
                continue

            # harus subclass agent
            if not issubclass(obj, AgentBaseModel):
                continue

            # skip abstract/base
            if obj is AgentBaseModel:
                continue

            if inspect.isabstract(obj):
                continue
            
            if not hasattr(obj, "agent"):
                continue

            print(f"[WORKER] valid -> {name}")

            instance = obj()
            return instance

    def execute_worker(self, mod: Any) -> None:
        """
        
        """
        worker: int = 0
        
        instance = self.filter_worker(mod)
                        
        worker += 1
        SharedState.cached["worker_db"][f"worker_{worker}"] = instance
    
    def scan_worker(self) -> Dict[str, List[str] | str]:
        """
        
        """
        import os
        import importlib
        
        if not "worker_db" in SharedState.cached.keys():
            SharedState.cached["worker_db"] = {}
        
        path = os.path.abspath(os.path.join(os.getcwd(), "providers"))
        agent_external = os.listdir(path)
        
        if not agent_external:
            return False
        
        for agent in agent_external:
            path_agent = os.path.join(path, agent)
            if os.path.isdir(path_agent):
                
                agent_name = f"providers.{agent}.main"
                module = importlib.import_module(name=agent_name)
                self.execute_worker(module)
                    
        return SharedState.cached["worker_db"]

class ProviderManager:
    def __init__(self) -> None:
        self._worker = ScanWorker()
        self._load()
        
    def _load(self, reload: bool = False) -> bool:
        if not "worker_db" in SharedState.cached.keys():
            self._worker.scan_worker()
        
        if reload:
            del SharedState.cached["worker_db"]
            self._worker.scan_worker()
        
        localState.is_loaded = True
        return True

    
    def run_worker(self, prompt: str) -> Tuple[int, str, Any]:
        """
        
        """
        for number, (worker, agent) in enumerate(SharedState.cached["worker_db"].items()):
            print(f"[WORKER]: Loading {number} at {worker}..")
            
            if not agent:
                print(f"[WORKER]: Failed to load {worker} at :\nNone")
                continue
            
            status, response = agent.agent(prompt=prompt)
            
            if status:
                print(f"[{number}:{worker}]: {response}")
                return {"at": number, "worker": worker, "response": response}
            
            else:
                print(f"[FAILED][{number}:{worker}]: {response}")
                continue
        
        print("[!] All of Agent used.\n[!] No response returned.")
    
