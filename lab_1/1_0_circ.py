import gmsh
import sys

gmsh.initialize()

gmsh.model.add("t1_0_2")

lc = 0.5e-2
gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
gmsh.model.geo.addPoint(.1, 0, 0, lc, 2)
gmsh.model.geo.addPoint(-.1, 0, 0, lc, 3)

gmsh.model.geo.addCircleArc(2, 1, 3, 1)
gmsh.model.geo.addCircleArc(3, 1, 2, 2)

gmsh.model.geo.addCurveLoop([1, 2], 1)
gmsh.model.geo.addPlaneSurface([1], 1)

gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(2)

gmsh.write("t1_0_circ.msh")
gmsh.write("t1_0_circ.geo_unrolled")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()