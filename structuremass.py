import math
import numpy as np

def check_pressure(p, r, t_1, sigma_yield):
    sigma_hoop = p * r / t_1
    t_min = p * r / sigma_yield
    return sigma_yield/sigma_hoop-1, t_min

def find_mass_structure(rho, r, t_1, l):
    return rho * ( 2 * math.pi * r * t_1 * l + 4 * math.pi * r ** 2 * t_1 )

def find_total_mass(mass_structure, other_mass):
    return mass_structure + other_mass

def euler_check(e, r, t_1, l, g, total_mass):
    i = math.pi * (r ** 3) * t_1
    sigma_critical = math.pi ** 2 * e * i / (2 * math.pi * r * t_1) / (l **2)
    sigma_wall = 6 * g * total_mass / (2 * math.pi * r * t_1)
    return sigma_critical, sigma_critical/sigma_wall - 1

def find_k(l, r, t_1, v):
    min_lambda = (12/(math.pi ** 4) * (l ** 4) / (r ** 2 * t_1 ** 2) * (1 - v**2)) ** (1/2)
    #print("lambda", min_lambda)
    # n = l / (min_lambda / 2)
    # n_up = math.ceil(n)
    # n_down = math.floor(n)
    # lambd_up = l * 2 / n_up
    # k_down = 10 ** 32
    # if n_down > 0:
    #     lambd_down = l * 2/ n_down
    #     k_down = lambd_down + 12/(math.pi ** 4) * (l ** 4) / (r ** 2 * t_1 ** 2) * (1 - v**2) / lambd_down
    # k_up = lambd_up + 12/(math.pi ** 4) * (l ** 4) / (r ** 2 * t_1 ** 2) * (1 - v**2) / lambd_up
    # return min(k_up, k_down)
    return min_lambda + 12/(math.pi ** 4) * (l ** 4) / (r ** 2 * t_1 ** 2) * (1 - v**2) / min_lambda

def shell_buck_check(e, v, t_1, l, p, r, k, g, total_mass):
    q = (10**5 - 10**5) / e * ( (r / t_1) ** 2 )
    sigma_crit = (1.983 - 0.983 * math.exp(-23.14 * q)) * k * (math.pi ** 2) * e / 12 / (1 - v ** 2) * (t_1 / l) ** 2
    sigma_wall = 6 * g * total_mass / (2 * math.pi * r * t_1)
    return sigma_crit, sigma_crit/sigma_wall - 1


r, l, t_1 = 0.225, 1.27, 10 * 10 ** (-4)
e, v, rho, sigma_yield = 74.5 * 10**9 , 0.3, 2760, 3.72 * 10**8
g = 9.80665
p = 5 * 10 ** 5 
other_mass = 387.67 + 715.68 + 10.17 * 18 * 10 ** (-3) + 8.424 #payload and stuff + skin (against meteorites) + attatchment + panel

print(check_pressure(p, r, t_1, sigma_yield))
mass_struc = find_mass_structure(rho, r, t_1, l)
print("Structure Mass", mass_struc)
mass_total = find_total_mass(mass_struc, other_mass)
print(mass_total)
print(euler_check(e, r, t_1, l, g, mass_total))
k = find_k(l, r, t_1, v)
print(shell_buck_check(e, v, t_1, l, p, r, k, g, mass_total))