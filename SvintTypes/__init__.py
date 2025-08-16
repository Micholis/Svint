from dataclasses import dataclass
from enum import Enum  

class EventTypes(Enum):
    SINGLE = 1
    MULTICALL = 2

@dataclass 
class SvintMulticallEvent:
    asyncCallback: bool
    name: str
    registeredBy: str
    pluginsWithListeners: list[str]
    callbacks: list[callable]
    eventType: EventTypes = EventTypes.MULTICALL

@dataclass 
class SvintSingleEvent:
    asyncCallback: bool
    name: str
    registeredBy: str
    pluginWithListener: str
    callback: callable
    eventType: EventTypes = EventTypes.SINGLE

@dataclass(frozen=True)
class CalledEvent:
    caller: str
    params: dict