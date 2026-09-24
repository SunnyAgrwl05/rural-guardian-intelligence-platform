from dataclasses import dataclass
@dataclass
class Route: agent:str; domain:str; risk:str; reason:str
class IntentRouter:
    def route(self,msg):
        t=msg.lower()
        health=["chest pain","breathing","unconscious","medicine","dose","prescription","diagnos","symptom","bleeding","poison"]
        disaster=["flood","cyclone","earthquake","landslide","fire","storm","evacuat","disaster","heavy rain"]
        agriculture=["crop","wheat","rice","paddy","soil","fertilizer","fertiliser","pest","fungus","harvest","farm","kheti","fasal","barish","rain"]
        education=["school","student","study","exam","learning","education"]
        if any(x in t for x in health): return Route("health-safety-agent","health","high","Potentially high-risk health request")
        if any(x in t for x in disaster): return Route("disaster-agent","disaster","high","Potential disaster/emergency context")
        if any(x in t for x in agriculture): return Route("agriculture-agent","agriculture","medium","Agriculture/crop context")
        if any(x in t for x in education): return Route("education-agent","education","low","Education context")
        return Route("general-agent","general","low","General request")
