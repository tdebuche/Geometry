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

def single_module_STCs(layer,vertices,irot,TCcount):
  vertices = reorganize_vertices(vertices,irot)
  #if TCcount == 12:
    #return single_HDmodule_STCs(layer,vertices)
  if TCcount == 3:
    return single_LDmodule_STCs(layer,vertices)

def single_LDmodule_STCs(layer,vertices):
  x_middle,y_middle = np.sum(np.array(vertices[0]))/len(vertices[0]),np.sum(np.array(vertices[1]))/len(vertices[1])
  STC0_X,STC0_Y = [vertices[0][0],vertices[0][1],x_middle,vertices[0][5]], [vertices[1][0],vertices[1][1],y_middle,vertices[1][5]]
  STC1_X,STC1_Y = [vertices[0][2],vertices[0][3],x_middle,vertices[0][1]], [vertices[1][2],vertices[1][3],y_middle,vertices[1][1]]
  STC2_X,STC2_Y = [vertices[0][4],vertices[0][5],x_middle,vertices[0][3]], [vertices[1][4],vertices[1][5],y_middle,vertices[1][3]]
  return [[STC0_X,STC0_Y],[STC1_X,STC1_Y],[STC2_X,STC2_Y]]



#def STCs_single_Module

#def TCs_single_Module
