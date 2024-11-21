import math

class hole:
    def __init__(self, coord, diameter):
        #creates a "hole" item.
        self.pos = coord
        self.dia = diameter
        self.area = (self.dia /2) **2 * math.pi
        self.r = 0
    
    def p_i_computation(self, f_x, f_z, m_y, n_holes, hole_of_inertia):
        p_x = f_x / n_holes
        p_z = f_z / n_holes
        p_m_y = m_y * self.dia 

        return True
    
    def p_o_computation(self, f_y, m_x, m_z):
        p_o = "dsds"
        return p_o


hole_cg = "dfsafdfa"

 
hole_of_inertia = (hole.dia /2) **2 * math.pi * ( (hole.pos[0] - hole_cg[0]) **2 + (hole.pos[1] -hole_cg[1]) **2 )