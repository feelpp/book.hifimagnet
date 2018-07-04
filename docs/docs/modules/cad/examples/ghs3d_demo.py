# Copyright (C) 2007-2015  CEA/DEN, EDF R&D, OPEN CASCADE
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

import salome
salome.salome_init()

from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)

from salome.smesh import smeshBuilder
smesh =  smeshBuilder.New(salome.myStudy)

# create a box
box = geompy.MakeBoxDXDYDZ(200., 200., 200.)
geompy.addToStudy(box, "box")

# create a mesh on the box
mgtetraMesh = smesh.Mesh(box,"box: MG-Tetra and MG-CADSurf mesh")

# create a MG_CADSurf algorithm for faces
MG_CADSurf = mgtetraMesh.Triangle(algo=smeshBuilder.MG_CADSurf)
MG_Tetra = mgtetraMesh.Tetrahedron(algo=smeshBuilder.MG_Tetra)

# compute the mesh
mgtetraMesh.Compute()

# End of script


