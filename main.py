import numpy as np
import math
import pandas as pd
import Methods.VariableSetup as Meth
import Methods.PullPushThrough as test

xls = pd.ExcelFile("Design.xls")  # excel to usable variable
xls = pd.read_excel(xls, sheet_name="Data")
x = xls["X"].tolist()
y = xls["Y"].tolist()
d = xls["D"].tolist()
h = xls["flange"].tolist()[3]
t2, t3 = xls["thickness"][0], xls["thickness"][1]
materials= [xls["material1"].tolist(), xls["material2"].tolist(), xls["material3"].tolist()] # E, G, Tau max, Sigma max
fastener = xls["bolt"].tolist()
f_x, f_y, f_z, m_x, m_y, m_z = xls["forces"].tolist()[0], xls["forces"].tolist()[1],xls["forces"].tolist()[2], xls["forces"].tolist()[3], xls["forces"].tolist()[4], xls["forces"].tolist()[5]
holes = []

for i in range(x):
    c = (x[i], y[i])
    d_buffer = d[i]
    holes.append(Meth.hole(c, d))

holes = np.array(holes)  # list to array
holes_cg = Meth.find_hole_cg(holes)  # computation cg
hole_inertia = Meth.hole_of_inertia(holes)  # hole of inertia
n = np.arange(holes)
total_force_squared = 0
for j in holes:
    j.find_pos_cg()
    j.find_r()
    j.p_i_computation(f_x, f_z, m_y, n, hole_inertia)
    j.p_o_computation(f_y,m_x, m_z, h, n, hole_inertia)
    pull_push_stress = test.pull_push_check(j, t2, t3)
    bearing_stress = test.bearing_check(j, t2)
    fastener_stress = test.fastener_check(j)
    total_force_squared = total_force_squared + j.p[0] ** 2 + j.p[1]**2 + j.p[2]**2
for k in holes:
    for l in materials:
        thermal_stress = test.thermal_loads(j, Young_Modulus=k[0], alpha_c_clamped=k[4], alpha_b_fastener=fastener[6], stiffness_area_fastener= math.pi * 4 * j.dia, force_ratio=(math.sqrt((k.p_i**2+k.p_o**2)/total_force_squared)))

