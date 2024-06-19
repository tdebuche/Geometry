import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

from Python_Geometry.Geometric_tools import item_list


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


plt.figure(figsize = (12,8))
plt.title(label =  'Layer '+str(Layer))
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')                            
for module_idx in range(len(Module_Vertices)):
    Xvertices= Module_Vertices[module_idx][0] +[Module_Vertices[module_idx][0][0]]
    Yvertices= Module_Vertices[module_idx][1] + [Module_Vertices[module_idx][1][0]]
	x,y = np.sum(np.array(Module_Vertices[module_idx][0]))/len(Module_Vertices[module_idx][0]),np.sum(np.array(Module_Vertices[module_idx][1]))/len(Module_Vertices[module_idx][1])
	plt.scatter((x+Xvertices[0])/2,(y+Yvertices[0])/2 ,color ="red")
    if args.UV == "yes":
	    u,v = Module_UV[module_idx][0],Module_UV[module_idx][1]
	    plt.annotate("("+str(u)+","+str(v)+")",(x-60,y-10),size =  '8')
    if args.irot == "yes":
	    rot = Module_irot[module_idx]
	    plt.annotate(str(rot),(x-60,y-10),size =  '8')
    plt.plot(Xvertices,Yvertices,color = "black")
plt.show()
