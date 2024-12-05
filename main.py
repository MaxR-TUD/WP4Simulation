import numpy as np
import math
import pandas as pd
import Methods.VariableSetup as Meth
import Methods.PullPushThrough as test
n = int(input("enter the number of holes"))
xls = pd.ExcelFile("GEOMETRY FILE.xlsx")  # excel to usable variable
xls = pd.read_excel(xls, sheet_name="Data")
x = xls["X"].tolist()[:n]
y = xls["Y"].tolist()[:n]
d = xls["D"].tolist()[:n]
h = xls["flange"].tolist()[3]
t2, t3 = xls["thickness"][0], xls["thickness"][1]
materials= [xls["material1"].tolist()[:5], xls["material2"].tolist()[:5], xls["material3"].tolist()[:5]] # E, G, Tau max, Sigma max
fastener = xls["bolt"].tolist()
f_x, f_y, f_z, m_x, m_y, m_z = xls["forces"].tolist()[0], xls["forces"].tolist()[1],xls["forces"].tolist()[2], xls["forces"].tolist()[3], xls["forces"].tolist()[4], xls["forces"].tolist()[5]
holes = []

for i in range(len(x)):
    c = (x[i], y[i])
    d_buffer = d[i]
    holes.append(Meth.hole(c, d_buffer))

holes = np.array(holes)  # list to array
holes_cg = Meth.find_hole_cg(holes)  # computation cg
for hole in holes:
    hole.find_pos_cg(hole_cg=holes_cg)
    hole.find_r()
midlines = Meth.find_midline_plate(holes) # intermediate step
hole_inertia = Meth.find_inertia(holes, midlines)  # hole of inertia


total_force_squared = 0
pull_push_stresses, bearing_stresses, fastener_stresses, thermal_stresses = [], [], [], []
for j in holes:
    j.p_i_computation(f_x, f_z, m_y, n, hole_inertia)
    j.p_o_computation(f_y, f_z, m_x, m_z, h, w, n, hole_inertia, midlines)
    pull_push_stress = test.pull_push_check(j, t2, t3)
    bearing_stress = test.bearing_check(j, t2)
    fastener_stress = test.fastener_check(j)

    total_force_squared = total_force_squared + j.p[0] ** 2 + j.p[1]**2 + j.p[2]**2
    pull_push_stresses.append(pull_push_stress)
    bearing_stresses.append(bearing_stress)
    fastener_stresses.append(fastener_stress)

for l in holes:
    for k in materials:
        thermal_stress = test.thermal_loads(l, Young_Modulus=k[0], alpha_c_clamped=k[4], alpha_b_fastener=fastener[6], stiffness_area_fastener= math.pi * 4 * l.dia, force_ratio=(math.sqrt((l.p_i**2+l.p_o**2)/total_force_squared)))
        thermal_stresses.append(thermal_stress)
# safety factors
allowable_stresses = []
Safety_pull_push = []
for h in materials:
    allowable_stresses.append(h[2:4])
for i in pull_push_stresses:
    SF1 = allowable_stresses[0][0] / i[0]
    SF2 = allowable_stresses[0][0] / i[1]
    Safety_pull_push.append([SF1,SF2])
Safety_fastener = []
for i in fastener_stresses:
    SF1 = allowable_stresses[0][0]/i[0]
    SF2 = allowable_stresses[0][1]/i[1]
    Safety_fastener.append([SF1, SF2])
Safety_bearing = []
for i in bearing_stresses:
    SF = allowable_stresses[0][0]/i
    Safety_bearing.append(SF)
print(f"pull push : {Safety_pull_push}\n fasteners : {Safety_fastener}\n Bearing : {Safety_bearing}")
