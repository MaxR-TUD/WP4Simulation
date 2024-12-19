import math
import numpy as np

r,l,t_1 = 1, 1, 1
e, i, v, rho, sigma_yield = 10 **9, 10**9, 0.3, 2999, 10**6
lambd = 2
g = 9.80665
p = 5 * 10*5


def check_pressure(p, r, t_1, sigma_yield):
    sigma_hoop = p * r / t_1
    t_min = p * r / sigma_yield
    return sigma_yield/sigma_hoop-1, t_min

def find_mass_structure(rho, r, t_1, l):
    return rho * 2 * math.pi * r * t_1 * l

def find_total_mass(mass_structure, other_mass):
    return mass_structure + other_mass

def euler_check(e, i, r, t_1, l, g, total_mass):
    sigma_critical = math.pi ** 2 * e * i / (2 * math.pi * r * t_1) / (l **2)
    sigma_wall = 6 * g * total_mass
    t_min = math.pi ** 2 * e * i / (2 * math.pi * r * sigma_wall) / (l **2)
    return sigma_critical/sigma_wall - 1, t_min

def find_k(l, r, t_1, v):
    min_lambda = (12/(math.pi ** 4) * (l ** 4) / (r ** 2 * t_1 ** 2) * (1 - v**2)) ** 1/2
    n = l / min_lambda
    n_up = math.ceil(n)
    n_down = math.floor(n)
    lambd_up = l / n_up
    lambd_down = l / n_down
    k_up = lambd_up + 12/(math.pi ** 4) * (l ** 4) / (r ** 2 * t_1 ** 2) * (1 - v**2) / lambd_up
    k_down = lambd_down + 12/(math.pi ** 4) * (l ** 4) / (r ** 2 * t_1 ** 2) * (1 - v**2) / lambd_down
    return min(k_up, k_down)



def shell_buck_check(e, v, t_1, l, p, r, k, g, total_mass):
    q = p / e * ( (r / t_1) ** 2 )
    sigma_crit = (1.983 - 0.983 * math.exp(-23.14 * q)) * k * (math.pi ** 2) * e / 12 / (1 - v ** 2) * (t_1 / l) ** 2
    sigma_wall = 6 * g * total_mass
    return sigma_crit/sigma_wall - 1
