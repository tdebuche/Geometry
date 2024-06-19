import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

from Python_Geometry.Geometric_tools import item_list


parser = argparse.ArgumentParser()
parser.add_argument("Layer", help="Layer to display",type=int)
parser.add_argument("--UV",default = 'no', help="With or without UV")
parser.add_argument("--STCs",default = 'no', help="With or without STCs")
parser.add_argument("--Record",default = 'no', help="Record all layers")
args = parser.parse_args()
Layer = args.Layer

Module_Vertices = item_list('Python_Geometry/src/Modules.json','vertices')
plt.figure(figsize = (12,8))
plt.title(label =  'Layer '+str(Layer))
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')                            
for module_idx in range(len(Module_Vertices)):
    Xvertices= Module_Vertices[module_idx][0] + Module_Vertices[module_idx][0][0]
    Yvertices= Module_Vertices[module_idx][1] + Module_Vertices[module_idx][1][0]
    plt.plot(Xvertices,Yvertices,color = "black")
