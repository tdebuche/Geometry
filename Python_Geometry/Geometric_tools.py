import numpy as np
import awkward as ak
import json

def item_list(jsonfile,item,layer):
  L = []
  with open(jsonfile,'r') as file:
    data = json.load(file)[layer-1]
  for module_idx in range(len(data)):
    if item =="id":
      L.append(data[module_idx]['id'])
    if item =="irot":
      L.append(data[module_idx]['irot'])
    if item =="TCcount":
      L.append(data[module_idx]['TCcount'])
    if item =="uv":
      L.append([data[module_idx]['u'],data[module_idx]['v']])
    if item =="vertices":
      L.append([data[module_idx]['verticesX'],data[module_idx]['verticesY']])
  return L


def reorganize_vertices(vertices,irot):
  #find the vertex 0
  y_min = vertices[1][0]
  idx_min = 0
  for vertex_idx in range(len(vertices[1])):
    if vertices[1][vertex_idx] < y_min :
      y_min = vertices[1][vertex_idx]
      idx_min = vertex_idx
  vertices[0] = [vertices[0][(vertex_idx+idx_min)%len(vertices[0])] for vertex_idx in range(len(vertices[0]))]
  vertices[1] = [vertices[1][(vertex_idx+idx_min)%len(vertices[0])]for vertex_idx in range(len(vertices[0]))]
  
  #rotate
  vertices[0] = [vertices[0][(vertex_idx+irot)%len(vertices[0])]for vertex_idx in range(len(vertices[0]))]
  vertices[1] = [vertices[1][(vertex_idx+irot)%len(vertices[0])]for vertex_idx in range(len(vertices[0]))]
  
  return vertices

def single_module_STCs(vertices,irot,TCcount):
  vertices = reorganize_vertices(vertices,irot)
  if TCcount == 12:
    return single_HDmodule_STCs(vertices)
  if TCcount == 3:
    return single_LDmodule_STCs(vertices)

def single_LDmodule_STCs(vertices):
  x_middle,y_middle = np.sum(np.array(vertices[0]))/len(vertices[0]),np.sum(np.array(vertices[1]))/len(vertices[1])
  STC0_X,STC0_Y = [vertices[0][0],vertices[0][1],x_middle,vertices[0][5]], [vertices[1][0],vertices[1][1],y_middle,vertices[1][5]]
  STC1_X,STC1_Y = [vertices[0][2],vertices[0][3],x_middle,vertices[0][1]], [vertices[1][2],vertices[1][3],y_middle,vertices[1][1]]
  STC2_X,STC2_Y = [vertices[0][4],vertices[0][5],x_middle,vertices[0][3]], [vertices[1][4],vertices[1][5],y_middle,vertices[1][3]]
  return [[STC0_X,STC0_Y],[STC1_X,STC1_Y],[STC2_X,STC2_Y]]

def single_HDmodule_STCs(vertices):
  STCs = []
  x_middle,y_middle = np.sum(np.array(vertices[0]))/len(vertices[0]),np.sum(np.array(vertices[1]))/len(vertices[1])
  for big_STC_idx in range(3):
    big_STC_X = [vertices[0][big_STC_idx * 2]]+[vertices[0][big_STC_idx * 2 + 1 ]]+[x_middle]+[vertices[0][(big_STC_idx * 2 + 5)% 6]]
    big_STC_Y = [vertices[1][big_STC_idx * 2]]+[vertices[1][big_STC_idx * 2 + 1 ]]+[y_middle]+[vertices[1][(big_STC_idx * 2 + 5)% 6]]
    x_middle0,y_middle0 = (big_STC_X[0] + big_STC_X[1])/2,(big_STC_Y[0] + big_STC_Y[1])/2
    x_middle1,y_middle1 = (big_STC_X[1] + big_STC_X[2])/2,(big_STC_Y[1] + big_STC_Y[2])/2
    x_middle2,y_middle2 = (big_STC_X[2] + big_STC_X[3])/2,(big_STC_Y[2] + big_STC_Y[3])/2
    x_middle3,y_middle3 = (big_STC_X[3] + big_STC_X[0])/2,(big_STC_Y[3] + big_STC_Y[0])/2
    x_center,y_center = np.sum(np.array(big_STC_X))/4,np.sum(np.array(big_STC_Y))/4
    STC0_X,STC0_Y = [big_STC_X[0],x_middle0,x_center,x_middle3], [big_STC_Y[0],y_middle0,y_center,y_middle3]
    STC1_X,STC1_Y = [big_STC_X[1],x_middle1,x_center,x_middle0], [big_STC_Y[1],y_middle1,y_center,y_middle0]
    STC2_X,STC2_Y = [big_STC_X[2],x_middle2,x_center,x_middle1], [big_STC_Y[2],y_middle2,y_center,y_middle1]
    STC3_X,STC3_Y = [big_STC_X[3],x_middle3,x_center,x_middle2], [big_STC_Y[3],y_middle3,y_center,y_middle2]
    STCs.append([STC0_X,STC0_Y])
    STCs.append([STC1_X,STC1_Y])
    STCs.append([STC2_X,STC2_Y])
    STCs.append([STC3_X,STC3_Y])
  return STCs 

def single_tileboard_STCs(layer,vertices,u,TCcount):
  Scint_Letter, Scint_Number = Scintillatortype(u,layer)
  return(ScintillatorSTCs(vertices,layer,Scint_Letter,Scint_Number))



def Scintillatortype(u,Layer): #Return the type of the Scintillator Modules[index], see CMS-HGC-ScintMB-Docs_V0_9 page 5
    if Layer > 33 and Layer < 38:
        if u %2 == 0:
            return ('J',8)
        if u%2 == 1:
            if Layer == 34:
                return('J',4)
            if Layer == 35:
                return('J',6)
            if Layer == 36:
                return('J',7)
            if Layer == 37:
                return('J',8)
    if Layer == 38 or Layer == 39:
        if u%4 == 0:
            return ('C',5)
        if u%4 == 1:
            return ('D',8)
        if u%4 == 2:
            return ('E',8)
        if u%4 == 3:
            if Layer == 38:
                return ('G',3)
            if Layer == 39:
                return ('G',5)
    if Layer > 39 and Layer <44:
        if u%4 == 0:
            return ('B',12)
        if u%4 == 1:
            return ('D',8)
        if u%4 == 2:
            return ('E',8)
        if u%4 == 3:
            if Layer == 40:
                return ('G',7)
            if Layer > 40 :
                return ('G',8)
    if Layer > 43:
        if u%5 == 0:
            return ('A',5)
        if u%5 == 1:
            return ('B',12)
        if u%5 == 2:
            return ('D',8)
        if u%5 == 3:
            return ('E',8)
        if u%5 == 4:
            if Layer < 47:
                return ('G',8)
            if Layer == 47 :
                return ('G',6)
        



def ScintillatorSTCs(Scintillator,Layer,Scint_Letter,Scint_Number):
    Scintillator = np.array(Scintillator)
    I = [2,3,0,1]
    L = []
    if Scint_Letter in ['J','K','D','E','G'] and Scint_Number > 5 :
        ratio = Scint_Number/8
        x1,y1 = (((Scintillator[0,I[0]]-Scintillator[0,I[1]]) /(ratio*2) +Scintillator[0,I[1]]),((Scintillator[1,I[0]]-Scintillator[1,I[1]])/(ratio*2)+Scintillator[1,I[1]]))
        x2,y2 = ((Scintillator[0,I[1]]+Scintillator[0,I[2]])/2,(Scintillator[1,I[1]]+Scintillator[1,I[2]])/2)
        x3,y3 = (((Scintillator[0,I[3]]-Scintillator[0,I[2]]) /(ratio*2) +Scintillator[0,I[2]]),((Scintillator[1,I[3]]-Scintillator[1,I[2]])/(ratio*2)+Scintillator[1,I[2]]))
        x4,y4 = ((Scintillator[0,I[3]]+Scintillator[0,I[0]])/2,(Scintillator[1,I[3]]+Scintillator[1,I[0]])/2)
        x,y = ((x1+x3)/2,(y1+y3)/2)
        L.append([[Scintillator[0,I[0]],x1,x,x4],[Scintillator[1,I[0]],y1,y,y4]])
        L.append([[Scintillator[0,I[1]],x2,x,x1],[Scintillator[1,I[1]],y2,y,y1]])
        L.append([[Scintillator[0,I[2]],x3,x,x2],[Scintillator[1,I[2]],y3,y,y2]])
        L.append([[Scintillator[0,I[3]],x4,x,x3],[Scintillator[1,I[3]],y4,y,y3]])
    if Scint_Letter in ['A','C']:
        ratio = Scint_Number/8
        x1,y1 = (((Scintillator[0,I[1]]-Scintillator[0,I[0]]) /(ratio*2) +Scintillator[0,I[0]]),((Scintillator[1,I[1]]-Scintillator[1,I[0]])/(ratio*2)+Scintillator[1,I[0]]))
        x2,y2 = ((Scintillator[0,I[1]]+Scintillator[0,I[2]])/2,(Scintillator[1,I[1]]+Scintillator[1,I[2]])/2)
        x3,y3 = (((Scintillator[0,I[2]]-Scintillator[0,I[3]]) /(ratio*2) +Scintillator[0,I[3]]),((Scintillator[1,I[2]]-Scintillator[1,I[3]])/(ratio*2)+Scintillator[1,I[3]]))
        x4,y4 = ((Scintillator[0,I[3]]+Scintillator[0,I[0]])/2,(Scintillator[1,I[3]]+Scintillator[1,I[0]])/2)
        x,y = ((x1+x3)/2,(y1+y3)/2)
        L.append([[Scintillator[0,I[0]],x1,x,x4],[Scintillator[1,I[0]],y1,y,y4]])
        L.append([[Scintillator[0,I[1]],x2,x,x1],[Scintillator[1,I[1]],y2,y,y1]])
        L.append([[Scintillator[0,I[2]],x3,x,x2],[Scintillator[1,I[2]],y3,y,y2]])
        L.append([[Scintillator[0,I[3]],x4,x,x3],[Scintillator[1,I[3]],y4,y,y3]])
    if Scint_Letter in ['J','K','D','E','G'] and Scint_Number <= 5 :
        x2,y2 = ((Scintillator[0,I[1]]+Scintillator[0,I[2]])/2,(Scintillator[1,I[1]]+Scintillator[1,I[2]])/2)
        x4,y4 = ((Scintillator[0,I[3]]+Scintillator[0,I[0]])/2,(Scintillator[1,I[3]]+Scintillator[1,I[0]])/2)
        L.append([[Scintillator[0,I[0]],Scintillator[0,I[1]],x2,x4],[Scintillator[1,I[0]],Scintillator[1,I[1]],y2,y4]])
        L.append([[Scintillator[0,I[2]],Scintillator[0,I[3]],x4,x2],[Scintillator[1,I[2]],Scintillator[1,I[3]],y4,y2]])
    if Scint_Letter == 'B' :
        ratio = Scint_Number/8
        x1,y1 = ((Scintillator[0,I[0]] * 2/3+Scintillator[0,I[1]]*1/3),(Scintillator[1,I[0]] * 2/3+Scintillator[1,I[1]]*1/3))
        x1bis,y1bis = ((Scintillator[0,I[0]] * 1/3+Scintillator[0,I[1]]*2/3),(Scintillator[1,I[0]] * 1/3+Scintillator[1,I[1]]*2/3))
        x2,y2 = ((Scintillator[0,I[1]]+Scintillator[0,I[2]])/2,(Scintillator[1,I[1]]+Scintillator[1,I[2]])/2)
        x3,y3 = ((Scintillator[0,I[2]] * 2/3+Scintillator[0,I[3]]*1/3),(Scintillator[1,I[2]] * 2/3+Scintillator[1,I[3]]*1/3))
        x3bis,y3bis = ((Scintillator[0,I[2]] * 1/3+Scintillator[0,I[3]]*2/3),(Scintillator[1,I[2]] * 1/3+Scintillator[1,I[3]]*2/3))
        x4,y4 = ((Scintillator[0,I[3]]+Scintillator[0,I[0]])/2,(Scintillator[1,I[3]]+Scintillator[1,I[0]])/2)
        x5,y5 = ((x1+x3bis)/2,(y1+y3bis)/2)
        x6,y6 = ((x1bis+x3)/2,(y1bis+y3)/2)
        L.append([[Scintillator[0,I[0]],x1,x5,x4],[Scintillator[1,I[0]],y1,y5,y4]])
        L.append([[x1,x1bis,x6,x5],[y1,y1bis,y6,y5]])
        L.append([[Scintillator[0,I[1]],x2,x6,x1bis],[Scintillator[1,I[1]],y2,y6,y1bis]])
        L.append([[Scintillator[0,I[2]],x3,x6,x2],[Scintillator[1,I[2]],y3,y6,y2]])
        L.append([[x3,x3bis,x5,x6],[y3,y3bis,y5,y6]])
        L.append([[Scintillator[0,I[3]],x4,x5,x3bis],[Scintillator[1,I[3]],y4,y5,y3bis]])
    return L



















  
