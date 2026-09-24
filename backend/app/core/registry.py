import json,importlib
from pathlib import Path
from dataclasses import dataclass
@dataclass
class Module: name:str; version:str; description:str; implementation:object; tools:list[str]; risky:bool
class ModuleRegistry:
    def __init__(self,root): self.root=Path(root); self.modules={}
    def discover(self):
        for mf in self.root.glob("*/module.json"):
            d=json.loads(mf.read_text()); impl=importlib.import_module(d["entrypoint"]); obj=impl.create_module()
            self.modules[d["name"]]=Module(d["name"],d["version"],d["description"],obj,d.get("tools",[]),d.get("risky",False))
        return self.modules
    def get(self,name): return self.modules.get(name)
