# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 10:19:14 2016

@author: bms115
"""
import numpy as np


def norm(vector):
    "Normalises a vector, provided that the vector has a non-zero magnitude."
    n = np.linalg.norm(vector)
    if n > 0:
        return vector / n
    else:
        return vector

def normal_vector(opticalelement, point):
    """Finds the normal vector to an optical element at a given point.  All
       normal vectors must be in the negative z direction.
    """
    # Check the curvature of the optical element.
    if opticalelement._curv == 0:
        return np.array([0., 0., -1])
    else:
        if norm(np.array(point) - opticalelement.centre())[2] > 0:
            return -norm(np.array(point) - opticalelement.centre())
        else:
            return norm(np.array(point) - opticalelement.centre())

def x_intercept(ray):
    "Finds the x intercept of a ray."
    length = 0 - ray.p()[0]
    distance = length / ray.d()[0]
    intercept = ray.p() + distance * ray.d()
    return intercept
