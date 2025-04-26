from enum import Enum

class ActionChoice(Enum):
    None_ = 0         # "None" es una palabra reservada en Python, se renombra
    KO = 1
    Bounce = 2
    TopLife = 3
    BottomLife = 4
    Damage = 5
    Cost = 6
    Trash = 7
    HideLife = 8
    ArrangeLife = 9
