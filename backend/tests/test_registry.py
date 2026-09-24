from pathlib import Path
from app.core.registry import ModuleRegistry
def test_registry():
    r=ModuleRegistry(str(Path(__file__).parents[1]/"app/modules")); r.discover(); assert "rural-guardian" in r.modules
