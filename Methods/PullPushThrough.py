import VariableSetup
import math


def pull_push_check(hole, r_i=0, t2=0, t3=0):  # hole is a hole retard
    stress_t2 = 2 * hole.po / (math.pi * r_i * t2)  # [Pa]
    stress_t3 = 2 * hole.po / (math.pi * r_i * t3)  # [Pa]
    return [stress_t2, stress_t3]


def bearing_check(hole, ):

    return


def thermal_loads(hole,) :
    E = 123
    alpha_b = 123
    alpha_c = 123
    Asm = 123
    phi = "?"
    Tmin = 273.64
    Tmax = 297.83
    Tspace = 2.7

    F_tMin = (alpha_c - alpha_b) * (Tmin - Tspace) * E * Asm * (1 - phi)
    F_tMax = (alpha_c - alpha_b) * (Tmax - Tspace) * E * Asm * (1 - phi)

    return {F_tMin, F_tMax} 