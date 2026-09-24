from app.agents.router import IntentRouter
def test_agriculture(): assert IntentRouter().route("wheat crop fungus").agent=="agriculture-agent"
def test_health():
    r=IntentRouter().route("chest pain medicine dose"); assert r.agent=="health-safety-agent" and r.risk=="high"
def test_disaster(): assert IntentRouter().route("village flood").agent=="disaster-agent"
