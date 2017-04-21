# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 10:29:19 2016

@author: bms115
"""
from math import pi


def rtpairs(R, N):
    """Creates a distribution of pairs of points in concentric circles
    
        Parameters
        ----------
        R: list_type
           A list of radii for the concentric circles.
        N: list_type
           A list of the number of anles for each radius.
    """
    for i in range(len(R)):
        for n in range(N[i]):
            yield R[i], 2. / N[i] * n * pi
            
def rtuniform(n,rmax,m):
    """Creates a uniform distribution of points within a circle.
        
        Parameters
        ----------
        n:    integer_type
              The number of concentric circles of points within the
              distribution.
        rmax: float_type
              The maximum radius of the distribution of points.
        m:    integer_type
              The rate at which the number of points per concentric circle
              increases.
    """
    rmax=float(rmax)
    two_pi = 2.*pi
    # Incrementing the radius outwards.
    for i in range(1, n+1):
        theta = 0.
        rad=rmax / n * i
        # Incrementing around the circle.
        for p in range((i * m) + 1):
            if p == 0: # Creates the central point.
                yield 0., 0.
            else:
                r, t = rad, theta
                theta += two_pi/(i * m)
                yield r, t
        
        