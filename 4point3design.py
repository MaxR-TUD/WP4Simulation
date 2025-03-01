import numpy as np
import math
import matplotlib.pyplot as plt

#inputs

p_axial = 1907 /2
p_tr = 1907 / 2 / 2
f_x = 1907 / 2 / 2
f_z = 4767 / 2 / 2
material = "Aluminium 2014-T6"
sigma_yield = 414 * ( 10 ** 6 )

w = 2 * ( 10 ** (-2) )
d = 1.3 * ( 10 ** (-2) )
t = 0.3 * ( 10 ** (-2) )
l = 3 * (10 ** (-2))
h = 0.8 * ( 10 ** (-2) )

#graphs

#Kt graph
#graph 1

Kt_vals1 = np.array([[1, 1.5, 2, 2.5, 2.9], [1, 0.999, 0.975, 0.94, 0.92]])
Kt_coeffs1 = np.polyfit(Kt_vals1[0], Kt_vals1[1], 3)
plot_kt1 = np.poly1d(Kt_coeffs1)

Kt_vals2 = np.array([[2.9, 3.0, 3.5, 3.9, 4.2, 4.4, 4.7, 4.8, 4.95], [0.92, 0.92, 0.916, 0.9, 0.88, 0.865, 0.82, 0.8, 0.76]])
Kt_coeffs2 = np.polyfit(Kt_vals2[0], Kt_vals2[1], 2)
plot_kt2 = np.poly1d(Kt_coeffs2)

if w / d <= 2.9:
    k_t = plot_kt1( w / d )
else:
    k_t = plot_kt2( w / d )




#Kbry Graph
Kbry_options = {0.06: np.array([[0.5,  1,  1.5,    2,  2.5,    3, 3.5, 4],\
                                [0, 0.68, 0.87, 0.95, 0.98, 0.99,   1, 1]]),\
                0.08: np.array([[0.5,  1,  1.5,    2,  2.5,    3,  3.5, 4],\
                                [0, 0.78, 0.99, 1.08, 1.12, 1.13, 1.14, 1.14]]),\
                0.1: np.array([[0.5,   1,  1.5,    2,  2.5,    3,  3.5, 4],\
                                [0, 0.85, 1.07, 1.17, 1.22, 1.24, 1.25, 1.25]]),\
                0.12: np.array([[0.5,  1,  1.5,    2,  2.5,    3,  3.5, 4],\
                                [0, 0.86, 1.12, 1.23, 1.28, 1.31, 1.32, 1.32]]),\
                0.15: np.array([[0.5,  1,  1.5,    2,  2.5,    3,  3.5, 4],\
                                [0, 0.88, 1.19, 1.32, 1.37, 1.40, 1.41, 1.42]]),\
                0.2: np.array([[0.5,   1,  1.5,    2,  2.5,    3,  3.5, 4],\
                                [0, 0.88, 1.27, 1.41, 1.47, 1.50, 1.51, 1.51]]),\
                0.3: np.array([[0.5,   1,  1.5,    2,  2.5,    3,  3.5, 4],\
                                [0, 0.88, 1.35, 1.51, 1.59, 1.62, 1.64, 1.64]]),\
                0.4: np.array([[0.5,   1,  1.5,    2,  2.5,    3,  3.5, 4],\
                                [0, 0.88, 1.36, 1.55, 1.65, 1.68, 1.70, 1.70]]),\
                0.6: np.array([[0.5,   1,  1.5,    2,  2.5,    3,  3.5, 4],\
                                [0, 0.88, 1.36, 1.59, 1.69, 1.73, 1.75, 1.75]])}

#change tOverD to one of the values in following array

tOverD_options = [0.06, 0.08, 0.1, 0.12, 0.15, 0.2, 0.3, 0.4, 0.6]

def round_to_nearest_option(x, y):
    if x <= y[0]:
        return y[0]
    elif x >= y[-1]:
        return y[-1]
    else:
        for i in range(len(y) - 1):
            if x < 1/2 * ( y[i] + y[i+1] ):
                g = y[i]
                break
            else:
                g = y[i+1]
        return g

rounded_tOverD = round_to_nearest_option( t / d , tOverD_options)
#print("t/d: ", t/d)
Kbry_vals = Kbry_options.get(rounded_tOverD)
Kbry_coeffs = np.polyfit(Kbry_vals[0], Kbry_vals[1], 4)

plot_bry = np.poly1d(Kbry_coeffs)

# evalute value from regression
k_bry = plot_bry( 1/2 * w / d )


#Kty Graph
aav = ( 8 / (w - math.sin(45 * math.pi / 180) * d ) ) + ( 4 / ( w - d ) ) # without t
aavabr = 6 / ( ( aav ) * d  )
#print(aavabr)

def kty(x):
    return -0.341518 * x ** 2 + 1.39628 * x - 0.00520833

# evaluate value from regression
k_ty = kty( aavabr )

#print(k_ty)


# find the p

p_u = k_t * ( w - d ) * t * sigma_yield

p_bry = k_bry * d * t * sigma_yield

p_ty = k_ty * d * t * sigma_yield

def min_pbry_pu():
    if p_bry <= p_u:
        return p_bry
    else:
        return p_u

r_a = p_axial / (min_pbry_pu())
#print(r_a)


r_tr = p_tr / p_ty
#print(r_tr)

def margin():
    ms = 1 / ( ( r_a ** 1.6 + r_tr ** 1.6 ) ** 0.625 ) - 1
    return ms
print("Safety Margin of the Hole of the lug")
print(margin())

sigma = f_z / 2 * l * l / 2 / (t * w ** 3 / 12) + f_x / 2 * l * t / 2 / (t ** 3 * w / 12) + 0.674 / h / 2 / (t * w)

print("Safety Margin of the Lug itself bending")
print(sigma_yield/sigma - 1)


def volume():
    vol = (l * w + 1 / 2 * math.pi * ( w / 2 )**2 - math.pi * (d/2) **2) * t * 2
    return vol
print("Volume of the part")
print(volume())