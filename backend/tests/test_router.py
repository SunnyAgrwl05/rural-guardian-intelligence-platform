from app.agents.router import IntentRouter

def test_agriculture():
    assert IntentRouter().route("wheat crop fungus").agent == "agriculture-agent"

def test_health():
    r = IntentRouter().route("chest pain medicine dose")
    assert r.agent == "health-safety-agent" and r.risk == "high"

def test_disaster():
    assert IntentRouter().route("village flood").agent == "disaster-agent"

def test_business():
    assert IntentRouter().route("small rural business market").agent == "rural-business-agent"

def test_voucher_abuse():
    r = IntentRouter().route("someone wants to resell exam voucher codes")
    assert r.agent == "voucher-license-abuse-monitor" and r.risk == "high"
