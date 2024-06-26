import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

from Python_Geometry.Geometric_tools import *


parser = argparse.ArgumentParser()
parser.add_argument("Layer", help="Layer to display",type=int)
parser.add_argument("--UV",default = 'no', help="With or without UV")
parser.add_argument("--irot",default = 'no', help="With or without rot")
parser.add_argument("--STCs",default = 'no', help="With or without STCs")
parser.add_argument("--Record",default = 'no', help="Record all layers")
args = parser.parse_args()
Layer = args.Layer

Module_Vertices = item_list('Python_Geometry/src/Modules.json','vertices',Layer)
Module_UV = item_list('Python_Geometry/src/Modules.json','uv',Layer)
Module_irot = item_list('Python_Geometry/src/Modules.json','irot',Layer)
Module_TCcount = item_list('Python_Geometry/src/Modules.json','TCcount',Layer)
STC_Vertices = item_list('Python_Geometry/src/STCs.json','vertices',Layer)
STC_indices = item_list('Python_Geometry/src/STCs.json','index',Layer)

plt.figure(figsize = (12,8))
plt.title(label =  'Layer '+str(Layer))
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
for STC_idx in range(len(STC_Vertices)):
	vertices = STC_Vertices[STC_idx]
	Xvertices= vertices[0] +[vertices[0][0]]
	Yvertices= vertices[1] +[vertices[1][0]]
	plt.plot(Xvertices,Yvertices,color = "red")
	x,y = np.sum(np.array(vertices[0]))/len(vertices[0]),np.sum(np.array(vertices[1]))/len(vertices[0])
	plt.annotate(str(STC_indices[STC_idx]),(x-20,y-10),size =  '5')
for module_idx in range(len(Module_Vertices)):
	irot = Module_irot[module_idx]
	TCcount = Module_TCcount[module_idx]
	if irot != 999:
		vertices = reorganize_vertices(Module_Vertices[module_idx],irot)
	else :
		vertices = Module_Vertices[module_idx]
	Xvertices= vertices[0] +[vertices[0][0]]
	Yvertices= vertices[1] +[vertices[1][0]]
	x,y = np.sum(np.array(vertices[0]))/len(vertices[0]),np.sum(np.array(vertices[1]))/len(vertices[0])
	plt.scatter((x+Xvertices[0])/2,(y+Yvertices[0])/2 ,color ="red")
	if args.UV == "yes":
	    u,v = Module_UV[module_idx][0],Module_UV[module_idx][1]
	    plt.annotate("("+str(u)+","+str(v)+")",(x-60,y-10),size =  '8')
	if args.irot == "yes":
	    plt.annotate(str(irot),(x-60,y-10),size =  '8')
	plt.plot(Xvertices,Yvertices,color = "black")

plt.show()
