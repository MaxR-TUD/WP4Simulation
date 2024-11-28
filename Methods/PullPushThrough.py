import VariableSetup
import math
import numpy as np

def pull_push_check(hole, t2=0, t3=0):  # hole is a hole retard
    stress_t2 = 2 * hole.p_o / (math.pi * hole.dia * t2)  # [Pa]
    stress_t3 = 2 * hole.p_o / (math.pi * hole.dia * t3)  # [Pa]
    return [stress_t2, stress_t3]


def bearing_check(hole, D2, t2):
    stress = hole.pi/(D2 * t2)
    return stress


def thermal_loads(hole, Young_Modulus, alpha_b_fastener, alpha_c_clamped, stiffness_area_fastener, force_ratio) :
    E = Young_Modulus
    alpha_b = alpha_b_fastener
    alpha_c = alpha_c_clamped
    Asm = stiffness_area_fastener
    phi = force_ratio
    Tmin = 273.64
    Tmax = 297.83
    Tspace = 2.7

    F_tMin = (alpha_c - alpha_b) * (Tmin - Tspace) * E * Asm * (1 - phi)
    F_tMax = (alpha_c - alpha_b) * (Tmax - Tspace) * E * Asm * (1 - phi)

    return {F_tMin, F_tMax} 