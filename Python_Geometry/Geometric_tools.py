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

#def STCs_single_Module

#def TCs_single_Module
