
import math
import numpy as np


def pull_push_check(hole, t2=0, t3=0):  # hole is a hole retard
    stress_t2 = 2 * hole.p_o / (math.pi * hole.dia * t2)  # [Pa]
    stress_t3 = 2 * hole.p_o / (math.pi * hole.dia * t3)  # [Pa]
    return [stress_t2, stress_t3]


def bearing_check(hole, t2):
    stress = hole.p_i/(hole.dia * t2)
    return stress


def fastener_check(hole):
    shear_stress = hole.p_i/(((hole.dia/2)** 2) * math.pi)  # Pa
    tension_stress = hole.p_o/(((hole.dia/2)** 2) * math.pi)  # Pa
    return [shear_stress, tension_stress]


def thermal_loads(hole, Young_Modulus, alpha_b_fastener, alpha_c_clamped, stiffness_area_fastener, force_ratio) :
    E = Young_Modulus
    alpha_b = alpha_b_fastener
    alpha_c = alpha_c_clamped
    Asm = stiffness_area_fastener
    phi = force_ratio
    Tmin = 273.64
    Tmax = 297.83
    Tassembly = 273.15 + 15

    Stress_tMin = (alpha_c - alpha_b) * (Tmin - Tassembly) * E * (1 - phi) * Asm
    Stress_tMax = (alpha_c - alpha_b) * (Tmax - Tassembly) * E * (1 - phi) * Asm

    return [Stress_tMin, Stress_tMax]
