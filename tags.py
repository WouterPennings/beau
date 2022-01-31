from dataclasses import dataclass
from enum import Enum, auto

class ValueType(Enum):
    String = auto()
    Integer = auto()

class TagType(Enum):
    Paragraph = auto()
    HeaderOne = auto()
    HeaderTwo = auto()
    HeaderThree = auto()
    HeaderFour = auto()
    HeaderFive = auto()
    Div = auto()
    Break = auto()

@dataclass
class Tag:
    tag: TagType
    type: int # 0 = Start, 1 = End, 2 = Void

@dataclass
class Value:
    value: str
    type: ValueType

@dataclass
class VariableIndex:
    identifier: str

@dataclass
class VariableAssign:
    identifier: str   
    value: str 

@dataclass
class Token:
    tag: any