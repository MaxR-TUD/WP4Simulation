import math
import numpy as np

class hole:
    def __init__(self, coord, diameter):
        #creates a "hole" item.
        self.pos = coord #tuple in (x, z)
        self.dia = diameter
        self.area = (self.dia /2) **2 * math.pi
        self.pos_cg = 0 # position in relation with centroid #tuple in (x*, z*)
        self.r = 0 # distance to centroid
        self.p = [0, 0, 0]
        self.p_i = 0
        self.p_o = 0

    #find position of hole relative to cg
    def find_pos_cg(self, hole_cg):
        z_star = (self.pos[1] - hole_cg[1])
        x_star = -1 * (self.pos[0] - hole_cg[0])
        self.pos_cg = (x_star, z_star)
    
    def find_r(self):
        self.r = ( self.pos_cg[0] ** 2 + self.pos_cg[1] ** 2 ) ** (1/2)

    #find in-plane forces
    def p_i_computation(self, f_x, f_z, m_y, n_holes, hole_of_inertia):
        p_x = f_x / n_holes
        p_z = f_z / n_holes
        p_m_y = m_y * self.area * self.r / hole_of_inertia[0]

        #decomposing p_m_y and adding it to the component forces
        if self.pos_cg[0] == 0:
            p_x += p_m_y * np.sign(self.pos_cg[1])
        elif self.pos_cg[0] > 0:
            alpha = math.atan( self.pos_cg[1] / self.pos_cg[0] )
            p_x += p_m_y * math.sin(alpha)
            p_z += -1 * p_m_y * math.cos(alpha)
        elif self.pos_cg[0] < 0:
            alpha = math.atan( self.pos_cg[1] / self.pos_cg[0] )
            p_x += -1 * p_m_y * math.sin(alpha)
            p_z += p_m_y * math.cos(alpha)

        self.p_i = (p_x ** 2 + p_z ** 2) ** (1/2)
        self.p[0] = p_x
        self.p[2] = p_z
    
    #find out-out-plane forces
    def p_o_computation(self, f_y, f_z, m_x, m_z, gap, l, n_holes, hole_of_inertia, midlines):
        p_o = f_y / n_holes

        if self.pos_cg[1] > 0:
            a = midlines[0]
        else:
            a = midlines[1]
        p_o += f_z / 2 * l * self.area * (self.pos[1] - a) / hole_of_inertia[1] #just xx for one plate

        if self.pos_cg[1] > 0:
            b = -1
        else:
            b = 1
        p_o += b * m_x / gap / n_holes

        self.p_o = p_o + m_z * self.area * self.pos_cg[0] / hole_of_inertia[2]
        self.p[1] = self.p_o

#Finding the centroid for the hole group
def find_hole_cg(holes):
    hole_cg_x = 0
    hole_cg_z = 0
    total_area = 0
    for hole in holes:    
        hole_cg_x += hole.area * ( hole.pos[0] )
        total_area += hole.area
    for hole in holes:
        hole_cg_z += hole.area * ( hole.pos [1] )

    hole_cg_x = hole_cg_x / total_area
    hole_cg_z = hole_cg_z / total_area
    return (hole_cg_x, hole_cg_z)

# hole_cg = find_hole_cg(holes)

#Count how many holes there are when reading from the txt file.

#finding midlines for each plate's hole of inertia calculatinos
def find_midline_plate(holes):
    midline_down = 0
    midline_up = 0
    n = 0
    for hole in holes:
        if hole.pos_cg[1] > 0:
            midline_up += hole.pos[1]
        else:
            midline_down += hole.pos[1]
        n += 1
    midline_down = midline_down / n
    midline_up = midline_up / n
    return (midline_up, midline_down)


#calculate "sum (Ar^2)"
def find_inertia(holes, midlines):
    moment_of_inertia = [0,0,0] #r, xx (for one plate), zz
    for hole in holes:
        moment_of_inertia[0] += hole.area * ( hole.r ** 2 )
        if hole.pos_cg[1] > 0:
            moment_of_inertia[1] += hole.area * ( (hole.pos[1] - midlines[0] )** 2 )
        moment_of_inertia[2] += hole.area * ( hole.pos_cg[0] ** 2 )
    return moment_of_inertia

# hole_of_inertia = find_inertia(holes)