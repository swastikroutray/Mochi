from enum import Enum


class PetState(str, Enum):
    NORMAL = "normal"
    CONCERNED = "concerned"
    ANGRY = "angry"
    HAPPY = "happy"
