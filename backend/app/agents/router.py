from dataclasses import dataclass

@dataclass
class Route:
    agent: str
    domain: str
    risk: str
    reason: str

class IntentRouter:
    def route(self, msg: str) -> Route:
        t = msg.lower()
        health = ["chest pain","breathing","unconscious","medicine","dose","prescription","diagnos","symptom","bleeding","poison"]
        disaster = ["flood","cyclone","earthquake","landslide","fire","storm","evacuat","disaster","heavy rain","heatwave","lightning"]
        agriculture = ["crop","wheat","rice","paddy","soil","fertilizer","fertiliser","pest","fungus","harvest","farm","kheti","fasal","barish","rain","irrigation"]
        education = ["school","student","study","exam","learning","education","teacher","scholarship"]
        business = ["business","market","selling","shop","small business","msme","loan","customer","rural enterprise"]
        abuse = ["voucher","license key","license code","coupon code","resale","resell","share code","bulk code","subscription key","exam voucher"]
        if any(x in t for x in health):
            return Route("health-safety-agent","health","high","Potentially high-risk health request")
        if any(x in t for x in disaster):
            return Route("disaster-agent","disaster","high","Potential disaster/emergency context")
        if any(x in t for x in abuse):
            return Route("voucher-license-abuse-monitor","compliance","high","Potential voucher/license misuse context")
        if any(x in t for x in agriculture):
            return Route("agriculture-agent","agriculture","medium","Agriculture/crop context")
        if any(x in t for x in education):
            return Route("education-agent","education","low","Education context")
        if any(x in t for x in business):
            return Route("rural-business-agent","business","low","Rural business context")
        return Route("general-agent","general","low","General request")
