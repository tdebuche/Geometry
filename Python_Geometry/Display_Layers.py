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


##########################################################  RECORD ###############################################################################################
"""

if args.Record == 'yes':
    if args.Bins == 'yes' and args.STCs == 'yes':
        os.chdir("./LayerswithbinswithSTCs")
        if args.Edges == 'no':
            os.chdir("./NoEdges")
        if args.Edges == 'yes':
            os.chdir("./Edges")
    if args.UV == 'yes':
        os.chdir("./LayerswithUV")  
    
    if args.STCs  == 'yes':
        os.chdir("./LayerswithSTCs")

    for k in range(0,34):
        if k <13:
            Layer = 2 *k+1
        else :
            Layer = k + 14
        Modules = G[Layer-1]
        if Layer >33:
            STC = STCLD[Layer-34]
            STCVertices = functions.STCtoSTCVertices(STCLD[Layer-34])
        if Layer <34 and Layer > 26:
            STC = STCHD[Layer-27]
            STCVertices = functions.STCtoSTCVertices(STCHD[Layer-27])
        plt.figure(figsize = (12,8))
        plt.title(label =  'Layer '+str(Layer))
        plt.xlabel('x (mm)')
        plt.ylabel('y (mm)')
        for i in range(len(ModuleVertices)):
            plt.plot(ModuleVertices[i][0] + [ModuleVertices[i][0][0]],ModuleVertices[i][1]+ [ModuleVertices[i][1][0]], color = 'black')
            x,y = 
            if args.UV == 'yes':
                plt.annotate('(' + str(uv[i][0]) +','+str(uv[i][1])+')',(x - 60,y -10),size =  '8')

        if args.STCs == 'yes':
            if Layer > 26:
                for i in range(len(STCVertices)):
                    for j in range(len(STCVertices[i])):
                        stc = STCVertices[i][j]
                        plt.plot(stc[0]+[stc[0][0]],stc[1]+[stc[1][0]],linewidth = 0.2,color  = 'blue') #STC

                
        plt.savefig('Layer '+str(Layer)+'.png')"""
