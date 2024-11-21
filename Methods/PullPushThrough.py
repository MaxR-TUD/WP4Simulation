import VariableSetup
import math


def pull_push_check(hole, r_o=0, r_i=0):  # hole is a hole retard
    stress = 2 * hole.po / (math.pi * (r_o ** 2 - r_i ** 2))  # [Pa]
    return stress
