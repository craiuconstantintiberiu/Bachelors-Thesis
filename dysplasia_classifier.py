from enum import Enum


class Dysplasia(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5


def classify_based_on_angle(angle):
    if angle < 90:
        return Dysplasia.E
    if angle < 97.5:
        return Dysplasia.D
    if angle < 102.5:
        return Dysplasia.C
    if angle < 105:
        return Dysplasia.B
    return Dysplasia.A
