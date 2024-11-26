import numpy as np
import math
import pandas as pd
import Methods.VariableSetup as Meth
n = input("Number of holes")
xls = pd.ExcelFile("Design.xls")
xls = pd.read_excel(xls, sheet_name="Data")
x = xls["X"].tolist()
y = xls["Y"].tolist()
d = xls["D"].tolist()
holes = []
for i in range(x):
    c = (x[i], y[i])
    d_buffer = d[i]
    holes.append(Meth.hole(c, d))
holes = np.array(holes)
holes_cg = Meth.find_hole_cg(holes)

    
