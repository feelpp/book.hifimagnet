# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.2.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
#sys.path.insert( 0, r'/home/feelpp/data/FUD5')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Box_1 = geompy.MakeBoxDXDYDZ(200, 200, 200)
Cylinder_1 = geompy.MakeCylinderRH(80, 300)
geompy.TranslateDXDYDZ(Cylinder_1, 100, 100, -20)
Cylinder_2 = geompy.MakeCylinder(O, OX, 80, 300)
geompy.TranslateDXDYDZ(Cylinder_2, 0, 100, 100)
Cut_1 = geompy.MakeCutList(Box_1, [Cylinder_1, Cylinder_2], True)
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["VERTEX"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["VERTEX"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Cut_1, geompy.ShapeType["FACE"])
[] = geompy.GetExistingSubObjects(Cut_1, True)
[] = geompy.GetExistingSubObjects(Cut_1, True)
Group_1 = geompy.CreateGroup(Cut_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(Group_1, [42, 62, 68, 56])
exported = geompy.ExportXAO(Cut_1, [Group_1], [], "", "testcube.xao")
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Box_1, 'Box_1' )
geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
geompy.addToStudy( Cylinder_2, 'Cylinder_2' )
geompy.addToStudy( Cut_1, 'Cut_1' )
geompy.addToStudyInFather( Cut_1, Group_1, 'Group_1' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_1 = smesh.Mesh(Cut_1)
NETGEN_2D3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_3D_Simple_Parameters_1 = NETGEN_2D3D.Parameters(smeshBuilder.SIMPLE)
NETGEN_3D_Simple_Parameters_1.SetNumberOfSegments( 15 )
NETGEN_3D_Simple_Parameters_1.LengthFromEdges()
NETGEN_3D_Simple_Parameters_1.LengthFromFaces()
isDone = Mesh_1.Compute()
Cut_1_1 = Mesh_1.GroupOnGeom(Cut_1,'Cut_1',SMESH.VOLUME)
Group_1_1 = Mesh_1.GroupOnGeom(Group_1,'Group_1',SMESH.FACE)
smesh.SetName(Mesh_1, 'Mesh_1')
try:
  Mesh_1.ExportMED( r'testcube.med', 0, SMESH.MED_V2_2, 1, None ,1)
except:
  print 'ExportToMEDX() failed. Invalid file name?'


## Set names of Mesh objects
smesh.SetName(NETGEN_2D3D.GetAlgorithm(), 'NETGEN_2D3D')
smesh.SetName(NETGEN_3D_Simple_Parameters_1, 'NETGEN 3D Simple Parameters_1')
smesh.SetName(Group_1_1, 'Group_1')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(Cut_1_1, 'Cut_1')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
