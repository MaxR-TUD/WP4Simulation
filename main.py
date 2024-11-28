import numpy as np
import math
import pandas as pd
import Methods.VariableSetup as Meth



xls = pd.ExcelFile("Design.xls")  # excel to usable variable
xls = pd.read_excel(xls, sheet_name="Data")
x = xls["X"].tolist()
y = xls["Y"].tolist()
d = xls["D"].tolist()
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
for j in holes:
    j.find_pos_cg()
    j.find_r()
    j.p_i_computation(f_x, f_z, m_y, n, hole_inertia)
    j.p_i_computation(f_y,m_x, m_z, h, n, hole_inertia)  #  TO DO : H
