import gmsh
import sys

gmsh.initialize()

gmsh.model.add("t1_0_2")

lc = 1e-2
gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
gmsh.model.geo.addPoint(.1, 0, 0, lc, 2)
gmsh.model.geo.addPoint(-.1, 0, 0, lc, 3)

gmsh.model.geo.addPoint(0, 0, .2, lc, 4)
gmsh.model.geo.addPoint(.1, 0, .2, lc, 5)
gmsh.model.geo.addPoint(-.1, 0, .2, lc, 6)

gmsh.model.geo.addCircleArc(2, 1, 3, 1)
gmsh.model.geo.addCircleArc(3, 1, 2, 2)

gmsh.model.geo.addCircleArc(5, 4, 6, 3)
gmsh.model.geo.addCircleArc(6, 4, 5, 4)

gmsh.model.geo.addLine(2, 5, 5)
gmsh.model.geo.addLine(3, 6, 6)

gmsh.model.geo.addCurveLoop([1, 2], 1)
gmsh.model.geo.addPlaneSurface([1], 1)

gmsh.model.geo.addCurveLoop([3, 4], 2)
gmsh.model.geo.addPlaneSurface([2], 2)

gmsh.model.geo.addCurveLoop([1, 6, -3, -5], 3)
gmsh.model.geo.addSurfaceFilling([3], 3)

gmsh.model.geo.addCurveLoop([2, 5, -4, -6], 4)
gmsh.model.geo.addSurfaceFilling([4], 4)

l = gmsh.model.geo.addSurfaceLoop([i + 1 for i in range(4)])
gmsh.model.geo.addVolume([l])

gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(3)

gmsh.write("t0_1.msh")
gmsh.write("t1_0_cyl.geo_unrolled")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()