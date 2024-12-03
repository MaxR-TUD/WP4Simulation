import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import Methods.VariableSetup as Meth
import Methods.PullPushThrough as test


xls = pd.ExcelFile("GEOMETRY FILE.xlsx")  # excel to usable variable
xls = pd.read_excel(xls, sheet_name="Data")
x = xls["X"].tolist()[:4]
y = xls["Y"].tolist()[:4]
d = xls["D"].tolist()[:4]
h = xls["flange"].tolist()[3]
t2, t3 = xls["thickness"][0], xls["thickness"][1]
materials= [xls["material1"].tolist(), xls["material2"].tolist(), xls["material3"].tolist()] # E, G, Tau max, Sigma max
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
hole_inertia = Meth.find_inertia(holes)  # hole of inertia
n = len(holes)

#heatmap
just_x = []
just_y = []

for i in range(len(x)):
    #creating axes for the heatmap
    if x[i] not in just_x:
        just_x.append(x[i])
    if y[i] not in just_y:
        just_y.append(y[i])

just_x.sort()
just_y.sort()

p_i_data = np.empty(shape = (len(just_y), len(just_x)))
p_o_data = np.empty(shape = (len(just_x), len(just_y)))
p_tot_data = np.empty(shape = (len(just_x), len(just_y)))

for j in holes:
    j.p_i_computation(f_x, f_z, m_y, n, hole_inertia)
    j.p_o_computation(f_y,m_x, m_z, h, n, hole_inertia)
    p_i_data[j.pos[1]][j.pos[0]] = j.p_i
    p_o_data[j.pos[1]][j.pos[0]] = j.p_o
    p_tot_data[j.pos[1]][j.pos[0]] = ( j.p_i ** 2 + j.p_o ** 2 ) ** (1/2)

fig, ax = plt.figure()
fig.canvas.draw()

ax.set_xticklabels(just_x)
ax.set_yticklabels(just_y)

p_i_map = seaborn.heatmap(p_i_data)
p_i_map.invert_yaxis()
plt.show()