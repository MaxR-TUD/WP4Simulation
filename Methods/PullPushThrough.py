import VariableSetup
import math


def pull_push_check(hole, r_i=0, t2=0, t3=0):  # hole is a hole retard
    stress_t2 = 2 * hole.po / (math.pi * r_i * t2)  # [Pa]
    stress_t3 = 2 * hole.po / (math.pi * r_i * t3)  # [Pa]
    return [stress_t2, stress_t3]


def bearing_check(hole, ):

    return