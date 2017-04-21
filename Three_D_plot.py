#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 01:01:42 2016

@author: barnabysandeford
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import raytracer as rt
reload(rt)

s = rt.SphericalRefraction(100,0.03,1.0,1.5,(1/0.03))
# Finding the paraxial focal point of the spherical optical element
F = rt.focal_point1(s)
# The output plane is automatically placed at the paraxial focal point of "s".
p=rt.OutputPlane(F, 10000)

def zx_plot(n, rmax, m):
    """Creates a z-x plot of a bundle of rays propogated through "s".
    
       Parameters
       ----------
       n:    integer_type
             The number of concentric circles of rays within the
             distribution.
       rmax: float_type
             The maximum radius of the distribution of rays.
       m:    integer_type
             The rate at which the number of rays per concentric circle
             increases.
    """
    bundle=rt.bundle(n, rmax, m)
    fig = plt.figure()
    ax = Axes3D(fig)
    for ray in bundle:
        "Loop that plots the z-x positions of the parallel rays."
        s.propagate_ray(ray)
        p.propagate_ray(ray)
        x = []
        y = []
        z = []
        for position in ray.positions:
            x.append(position[0]) # Appends all x positions to the list "x".
            y.append(position[1]) # Appends all y positions to the list "y".
            z.append(position[2]) # Appends all z positions to the list "z".
        ax.plot(xs = z,ys = y,zs = x)
        
zx_plot(10,40,4)
