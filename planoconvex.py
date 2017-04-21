"""
Modelling a planoconvex singlet lens.
"""
import numpy as np
import matplotlib.pyplot as plt
import raytracer as rt

# Defining the planoconvex lens with the curved surface first, with a 
# refractive index of 1.5168.
convex = rt.SphericalRefraction(100, 0.02, 1.0, 1.5168, 21.8 )
plane1 = rt.SphericalRefraction(105, 0, 1.5168, 1.0, 21.8)
# Defining the planoconvex lens with the curved surface last.
concave = rt.SphericalRefraction(105, -0.02, 1.5168, 1.0, 21.8 )
plane2 = rt.SphericalRefraction(100, 0, 1.0, 1.5168, 21.8)
# Defining the wavelength of the incident rays.
L = (588*10**(-9))

def zxPlot(n, rmax, m , lens1, lens2):
    """ Creates a plot in the z-x plane of a bundle of rays through two optical
        elements.  The optical elements can be chosen such that they form
        planoconvex lenses.
        
        Parameters
        ----------
        n:    integer_type
              The number of concentric circles of rays within the
              distribution.
       rmax:  float_type
              The maximum radius of the distribution of rays.
       m:     integer_type
              The rate at which the number of rays per concentric circle
              increases.
       lens1: instance_type
              An optical element as defined in the raytracer module, and is the
              first optical element that the bundle is propagated through.
       lens2: instance_type
              An optical element as defined in the raytracer module, and is the
              second optical element that the bundle is propagated through.
    """
    bundle = rt.bundle(n, rmax, m)
    # Defining the output plane to be at the focal point of the combination of 
    # lens1 and lens2.  An arbitrarily large aperture radius was chosen to
    # ensure that all rays were incident on the plane. 
    output_plane = rt.OutputPlane(rt.focal_point2(lens1, lens2), 10000)
    for ray in bundle:
        lens1.propagate_ray(ray)
        lens2.propagate_ray(ray)
        output_plane.propagate_ray(ray)
        x = []
        z = []
        for position in ray.positions:
            x.append(position[0])
            z.append(position[2]) 
        plt.plot(z,x)
    plt.xlabel('z axis /mm')
    plt.ylabel('x axis /mm')
    plt.show()

def xypositions(n, rmax, m, lens1, lens2):
    """Creates a list of the x-y positions of the rays incident on the output
       plane.
       
       Parameters
       ----------
       n:     integer_type
              The number of concentric circles of rays within the
              distribution.
       rmax:  float_type
              The maximum radius of the distribution of rays.
       m:     integer_type
              The rate at which the number of rays per concentric circle
              increases.
       lens1: instance_type
              An optical element as defined in the raytracer module, and is the
              first optical element that the bundle is propagated through.
       lens2: instance_type
              An optical element as defined in teh raytracer module, and is the
              second optical element that the bundle is propagated through.
    """
    # Placing the output plane at the focal point of lens1 and lens2.
    output_plane = rt.OutputPlane(rt.focal_point2(lens1, lens2), 10000)
    positions = []
    bundle=rt.bundle(n, rmax, m)
    for ray in bundle:
        lens1.propagate_ray(ray)
        lens2.propagate_ray(ray)
        output_plane.propagate_ray(ray)
        x = []
        y = []
        x.append(ray.positions[-1][0]) # Appends the last x position to "x".
        y.append(ray.positions[-1][1]) # Appends the last y position to "y".
        positions.append([x[0],y[0]]) # Creates a list of x-y coordinates.
    return positions

def rootmean(list1):
    """ Finds the root mean square radial deviation of a list of x-y positions.
    
        Parameters
        ----------
        list1: list_type
               List of x-y positions.
    """
    r_squares = []
    for position in list1:
        # Finding the square of the radial displacement.
        r2 = (position[0] * position[0]) + (position[1] * position[1])
        r_squares.append(r2)
    mean=sum(r_squares)/len(r_squares)
    rms=np.sqrt(mean)
    return rms
    

# Plotting the ray bundle propagation in the z-x plane for the plane surface
# first.
plt.figure(0)
plt.title('Plane surface first')
zxPlot(10, 5, 6, plane2, concave)
# Plotting the ray bundle propagation in the z-x plane for the convex surface
# first.
plt.figure(1)
plt.title('Convex surface first')
zxPlot(10, 5, 6, convex, plane1)
# To find the marginal ray focal points, change the bundle ray attributes to 
# (2, 21.79, 4) and re-run the scirpt. Zoom in on the focal point and use the 
# cursor to identify the position of the focal point.

print 'Convex first:'  
list1 = xypositions(10,5,6, convex, plane1)
print 'The rms radius = ', rootmean(list1), 'mm'
diffraction_limited = L * (rt.focal_point2(convex, plane1) - 105) / (10**(-2))
print 'The diffraction-limited radius = ', diffraction_limited,'mm'

print ' \n Plane first:'
list2 = xypositions(10,5,6, plane2, concave)
print 'The rms radius =', rootmean(list2), 'mm'
diffraction_limited = L * (rt.focal_point2(plane2, concave) - 105) / (10**(-2))
print 'The diffraction-limited radius =', diffraction_limited, 'mm'
    