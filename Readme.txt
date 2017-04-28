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

single_surface and planoconvex use the other modules to carry out some tasks using the code.  They both propagate light rays through various types and set-ups of lenses.  Single surface just creates the one optical lens.  If without changing anything, you run the single_surface script, it creates three graph-plots, and gives out the root mean square (rms) focal radius at the paraxial focal point of a lens, and the diffraction-limited focal radius.  Figure 1 is a z-x plot of the ray propagation, figure 2 is a spot diagram at the paraxial focal point, and figure 3 shows the variation of the rms focal radius and diffraction-limited focal radius with the beam diameter for a range of wavelengths. Figure 3 takes a few seconds to generate as it has a fair few calculations to do.

planoconvex propagates light rays through two types of planconvex lenses.  The first one has the curved surface facing the incoming rays, and the other has the flat surface first.  All of the optical elements have been pre-defined to make planoconvex lenses.  “convex” and “plane1” combine to make a plano-convex lens with the curved surface facing the incident rays of light. “concave” and “plane2” form another plano-convex lens with the flat side facing the incident rays. The wavelength and refractive indexes are predefined, but can be adjusted. If you run the code without changing anything, it creates 2 plots and gives the rms and diffraction-limited radii for both orientations. Figure 0 is the ray propagation plot for the convex-first case, and figure 1 is for the plane-first case.  Feel free to change the attributes of the variables or functions to see what happens. For instance, changing the ray bundle’s distribution alters the rms values.
