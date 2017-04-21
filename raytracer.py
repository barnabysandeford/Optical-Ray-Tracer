# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 15:24:37 2016

@author: bms115
"""
import numpy as np
from math import cos,sin
import genpolar
import vector_math as vm
from vector_math import norm, normal_vector


class Ray:  
    """
    Creates a light ray. Each light ray is initialised with a position and a 
    direction vector.
    """
    
    def __init__(self, p=[0., 0., 0.], k=[0., 0., 0.]):
        """
        Initialises the Ray class.
        
        Parameters
        --------------
        p: list_like
        First argument, is the position vector.
       
        k: list_like
        Second argument, is the direction vector.
        """
        p, k = np.array(p), norm(np.array(k))        
        positions = []
        directions = []
        self.positions = positions
        self.directions = directions
        positions.append(p)
        directions.append(k)
        
    def p(self):
        """
        p: Finds the last known position of the light ray from the list of
             positions.
        """
        return self.positions[-1]

    def d(self):
        """
        d: Finds the last known direction of the light ray from the list of
             directions.
        """
        return self.directions[-1]

    def append_point(self, point):
        """
        It appends a point to the list of positions.

        Parameters
        ----------
        point: list_like

        """
        self.positions.append(np.array(point))

    def append_vector(self, vector):
        """
        It appends a vector to the list of directions.

        Parameters
        ----------
        vector: list_like 

        """
        self.directions.append(norm(np.array(vector)))

    def __repr__(self):
        return 'r=(%s, %s)' % (self.p().__repr__(), self.d().__repr__())


class OpticalElement:
    """
    Creates some kind of optical element. The optical element is a surface
    that could collect, relect or refract incident rays.
    """

    def propagate_ray(self, other):
        "Propogates a ray through some optical element."
        raise NotImplementedError()


class SphericalRefraction(OpticalElement):
    """
        Creates an optical element that is a curved surface, which is
        defined by 5 parameters.
    """

    def __init__(self, z0, curv, n1, n2, ap_r):
        """
        Initialises the SphericalRefraction class.

        Parameters
        ----------
        z0:   float_type
              The z axis intercept of the curved surface.
        curv: float_type
              The curvature of the surface or the reciprocal of the radius
              of curvature.
        n1:   float_type
              The refractive index to the left of the optical element.
        n2:   float_type
              The refractive index to the right of the optical element.
        ap_r: float_type
              The aperture radius of the optical element, or how far either
              side of the z axis it extends.
        """
        self._z0 = float(z0)
        self._curv = float(curv)
        self._n1 = float(n1)
        self._n2 = float(n2)
        self._ap_r = float(ap_r)

    def centre(self):
        """Finds the centre of the spherical object, as long as the curvature
           isn't zero."""
        if self._curv == 0.:
            raise Exception('This is a plane surface.')
        else:
            return np.array([0., 0., self._z0 + (1 / self._curv)])

    def rad_curv(self):
        """
        Finds the radius of curvature of the optical element.
        """
        return 1 / np.absolute(self._curv)

    def intercept(self, ray):
        """
        Finds the interception point of a ray with the optical element.
        """
        r2 = self._ap_r**2
        k = ray.d()
        p = ray.p()
        if self._curv == 0:
            # Distance between the ray's start point and the plane.
            length = (self._z0 - p[2]) / k[2]
            x2 = (p + k * length)[0]**2
            y2 = (p + k * length)[1]**2
            # Check if the ray intercepts within the aperture radius.
            if x2 + y2 <= r2:
                return (p + k * length)
            else:
                return 'no intercept'
        else:
            r = ray.p() - self.centre()
            R = self.rad_curv()
            dot = np.dot(r, k)
            if ((dot * dot) - (np.dot(r, r) - (R * R))) < 0:
                return 'no intercept'
            else:
                L1 =- dot + np.sqrt((dot * dot) - (np.dot(r, r) - (R * R)))
                L2 =- dot - np.sqrt((dot * dot) - (np.dot(r, r) - (R * R)))  
                a2 = (p + k * L1)[0]**2
                b2 = (p + k * L1)[1]**2
                c2 = (p + k * L2)[0]**2
                d2 = (p + k * L2)[1]**2
                if self._curv > 0:
                    # For positive curvature, the closer intercept is wanted.
                    if L1 < L2:
                        if (a2 + b2 <= r2):
                            return ray.p() + ray.d() * L1
                        else:
                            return 'no intercept'
                    else:
                        if (c2 + d2 <= r2):
                            return ray.p() + ray.d() * L2
                        else:
                            return 'no intercept'
                if self._curv < 0:
                    # For negative curvature, the further intercept is wanted.
                    if L1 < L2:
                        if (c2 +d2 <= r2):
                            return ray.p() + ray.d() * L2
                        else:
                            return 'no intercept'
                    else:
                        if (a2 + b2 <= r2):
                            return ray.p() + ray.d() * L1
                        else:
                            return 'no intercept'
                 
    def propagate_ray(self, ray):
        """
        Propagates a ray from its starting position, to the optical element,
        appends all new positions to the ray, and all new directions through
        refraction to the ray. Stops if the ray doesn't intercept with an
        optical element, or is reflected at the boundary.
        """
        if type(self.intercept(ray)) == np.ndarray:
            ray.append_point(self.intercept(ray))
        #Delete this alteration of putting the next section inside the if 
        #statement if it doesn't work
            normal = normal_vector(self, self.intercept(ray))
            if type(refract(ray, normal, self._n1, self._n2)) == np.ndarray:
                ray.append_vector(refract(ray, normal, self._n1, self._n2))


class OutputPlane(OpticalElement):

    def __init__(self, z0, ap_r):

        """
        Initialises the OutputPlane class.

        Parameters
        ----------
        z0:   float_type
              The z axis intercept of the curved surface.
        ap_r: float_type
              The aperture radius of the optical element, or how far either
              side of the z axis it extends.
        """
        self._z0 = float(z0)
        self._ap_r = float(ap_r)

    def intercept(self, ray):
        """
        Finds the interception point of a ray with the output plane.
        """
        k = ray.d()
        p = ray.p()
        length = (self._z0 - p[2]) / k[2]
        r2 = self._ap_r**2
        x2 = (p + k * length)[0]**2
        y2 = (p + k * length)[1]**2
        # Check if the intercept is within the aperture radius.
        if x2 + y2 <= r2:
            return (p + k * length)
        else:
            return 'no intercept'

    def propagate_ray(self, ray):
        """
        Propagates a ray from its starting position, to the output plane and
        appends the new position to the ray. Stops if the ray doesn't
        intercept with the output plane.
        """
        if type(self.intercept(ray)) == np.ndarray:
            ray.append_point(self.intercept(ray))


def refract(incident, normal, n1, n2):
    """
    Finds the resulting refracted ray at a boundary. Returns nothing if the 
    ray is reflected.

    Paramters
    ---------
    incident: instance_type
              Ray object. It is the incident ray on the boundary.
    normal:   numpy.array_type
              The normal vector to the boundary.
    n1:       float_type
              The refractive index to the left of the boundary.
    n2:       float_type
              The refractive index to the right of the boundary.
    """
    n1 = float(n1)
    n2 = float(n2)
    r = n1 / n2
    dot = -np.dot(normal, incident.d())
    # Check if the ray is reflected.
    if np.sqrt(1 - (dot * dot)) > n2/n1:
        return 'no refraction'
    else:
        if normal[2] < 0:
            refracted = (r * incident.d() + normal * (
                r * dot - np.sqrt(1 - (r * r) * (1 - (dot*dot)))
                ))
            return norm(refracted)
        else:
            raise Exception('Normal vector not in the negative z direction.')


def bundle(n, rmax, m):
    """Creates a uniform bundle of parallel rays with radius rmax, n concentric
       circles, m points per circle. Returns a list, rays, of all the rays.
       
       Parameters:
       -----------
       n:    integer_type
             The number of concentric circles of rays within the
             distribution.
       rmax: float_type
             The maximum radius of the distribution of rays.
       m:    integer_type
             The rate at which the number of rays per concentric circle
             increases.
    """
    x = []
    y = []
    rays = []
    # Use the genpolar module to create a uniform distribution of rays.
    for r, t in genpolar.rtuniform(n, rmax, m):
        x.append(r * cos(t))
        y.append(r * sin(t))
    for n in range(len(x)):
        rays.append(Ray([x[n], y[n], 0], [0., 0., 1.]))
    return rays


def focal_point1(opticalelement):
    """ Finds the paraxial focal point for an optical element by propagating
        a ray in the positive z direction, 0.1mm from the z axis, through the
        optical element, and finding its z axis intercept.
    """
    # Use a ray close to the z axis to find the paraxial focal point.
    r = Ray([0.1, 0, 0], [0, 0, 1])
    opticalelement.propagate_ray(r)
    return vm.x_intercept(r)[2]


def focal_point2(opticalelement1, opticalelement2):
    """ Finds the paraxial focal point for two optical elements by propagating
        a ray in the positive z direction, 0.1mm from the z axis, through the
        optical elements, and finding its z axis intercept.
    """
    r = Ray([0.1, 0, 0], [0, 0, 1])
    opticalelement1.propagate_ray(r)
    opticalelement2.propagate_ray(r)
    return vm.x_intercept(r)[2]