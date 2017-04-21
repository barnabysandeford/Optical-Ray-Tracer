"""This is the script for the "Getting started" section.  All optical elements
   are as stated in the project guide.
"""
import numpy as np
import matplotlib.pyplot as plt
import raytracer as rt

s = rt.SphericalRefraction(100,0.03,1.0,1.5,(1/0.03))
# Calculating the paraxial focal point of "s".
F = rt.focal_point1(s)
# The output plane is automatically placed at the paraxial focal point of "s".
p=rt.OutputPlane(F, 10000)
# Defining the wavelength of the rays.
Lb = 475 * 10**(-9) # Blue light
Lg = 510 * 10**(-9) # Green light
Lr = 650 * 10**(-9) # Red light


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
    for ray in bundle:
        "Loop that plots the z-x positions of the parallel rays."
        s.propagate_ray(ray)
        p.propagate_ray(ray)
        x=[]
        z=[]
        for position in ray.positions:
            x.append(position[0]) # Appends all x positions to the list "x".
            z.append(position[2]) # Appends all y positions to the list "y".
        plt.plot(z,x)
    plt.xlabel('z axis /mm')
    plt.ylabel('x axis /mm')
    plt.show()

def spotdiagram(n, rmax, m):
    """Plots the spot diagram of the rays incident on the output
       plane.
       
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
    bundle = rt.bundle(n, rmax, m)
    for ray in bundle:
        s.propagate_ray(ray)
        p.propagate_ray(ray)
        x = []
        y = []
        x.append(ray.positions[-1][0]) # Appends the last x position to "x".
        y.append(ray.positions[-1][1]) # Appends the last y position to "y".
        plt.plot(x,y, 'bo')
    plt.xlabel('x axis /mm')
    plt.ylabel('y axis /mm')
    plt.show()
    plt.axis('auto')
   
def xypositions(n, rmax, m):
    """Creates a list of the x-y positions of the rays incident on the output
       plane.
       
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
    positions = []
    bundle = rt.bundle(n, rmax, m)
    for ray in bundle:
        s.propagate_ray(ray)
        p.propagate_ray(ray)
        x = []
        y = []
        x.append(ray.positions[-1][0]) # Appends the last x position to "x".
        y.append(ray.positions[-1][1]) # Appends the last y position to "y".
        positions.append([x[0],y[0]]) # Creates a list of x-y coordinates.
    return positions 

def focalradius_plot():
    """Creates a graph of the diameter of incident ray bundles on "s" (defined
       above), against the rms focal point radius, and the diffraction limited 
       focal point radius.
    """
    D = [] # List of the ray bundle radii.
    rms = []  # List of the rms focal point radii.
    # Lists of the diffraction limited focal point radii.
    diffraction_blue = []  
    diffraction_green = []
    diffraction_red = []
    focal_length = F - 100
    for n in range(10,90):
        # Incrementing the radius of the bundle.
        d = n * 0.1 
        two_d = 2 * d
        two_d_metres = (2 * d / 1000) # Gives units of metres.
        list1 = xypositions(6, d, 6)
        root_mean = rootmean(list1)
        # Calculating the diffraction scale.
        b = Lb * (focal_length) / (two_d_metres) 
        g = Lg * (focal_length) / (two_d_metres)
        r = Lr * (focal_length) / (two_d_metres)
        D.append(two_d)
        rms.append(root_mean)
        diffraction_blue.append(b)
        diffraction_green.append(g)
        diffraction_red.append(r)
    plt.plot(D, rms, 'k', label='Root mean square spot radius' )
    plt.plot(D, diffraction_blue, 'b', label = ('Diffraction-limited radius '
                                                            +'for blue light'))
    plt.plot(D, diffraction_green, 'g', label = ('Diffraction-limited radius '
                                                            +'for green light'))
    plt.plot(D, diffraction_red, 'r', label = ('Diffraction-limited radius '
                                                            +'for red light'))
    plt.legend()
    plt.xlabel('Ray bundle diameter /mm')
    plt.ylabel('Spot radius /mm')
    plt.show()

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
    
    
# Plotting the propagation of the rays through the optical elements.
plt.figure(1)
zx_plot(10,2.5,5)
# Tracing a bundle of rays (diameter of 5mm) to the paraxial focus point. 
plt.figure(2)
plt.axis('equal')
spotdiagram(10, 2.5, 5)
# Creating a list of the positions in the spot diagram.
list1 = xypositions(10, 2.5, 5)
# Giving a value of the rms value for this focus point.
print 'Root mean square spot radius = ', rootmean(list1)
# Calculating the diffraction scale, adjusting the diameter to be in metres.
diffraction_scale = (Lg) * (F - 100) / (5 * 10**(-3)) 
print 'Diffraction limited spot radius for green light = ', diffraction_scale
# Creating a graph of the ray bundle diameter vs the focal point radii.
plt.figure(3)
focalradius_plot()
