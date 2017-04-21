Read me:

This explains how to use the following modules to carry out the Optical Ray Tracer programme.  The modules that make up the programme are:

1. raytracer.py
2. vector_math.py
3. genpolar.py
4. single_surface.py
5. planoconvex.py

raytracer contains the bulk of the code, but nothing needs to be done with it in order to carry out the script. The module contains the most important classes, and some of the useful functions.

vector_math contains some useful mathematical functions that are better suited in their own module, and are imported into raytracer to facilitate some of the code.

genpolar is only required to facilitate the bundle function in raytracer, and was originally created in its own module, so was kept that way.

single_surface carries out the “getting started” part of the code. All of the surfaces are already defined for you, but you can change them around if you like.  If without changing anything, you run the code, it creates three plots, and gives out the root mean square (rms) focal radius at the paraxial focal point, and the diffraction-limited focal radius.  Figure 1 is a z-x plot of the ray propagation, figure 2 is the spot diagram at the paraxial focal point, and figure 3 shows the variation of the rms focal radius and diffraction-limited focal radius with the beam diameter for a range of wavelengths. Feel free to adjust the increment, d, of the “focalradius_plot” function to see how the graph changes, or change the wavelengths plotted to see what happens. Figure 3 takes a few seconds to generate as it has a fair few calculations to do.

planoconvex carries out the second part of the lab script. Again, all of the optical elements have been pre-defined to make planoconvex lenses.  “convex” and “plane1” combine to make a llano-convex lens with the curved surface facing the incident rays of light. “concave” and “plane2” form another plano-convex lens with the flat side facing the incident rays. The wavelength and refractive indexes are predefined, but can be adjusted. If you run the code without changing anything, it creates 2 plots and gives the rms and diffraction-limited radii for both orientations.  Figure 0 is the ray propagation plot for the convex-first case, and figure 1 is for the plane-first case.  Feel free to change the attributes of the variables or functions to see what happens. For instance, changing the ray bundle’s distribution alters the rms values.