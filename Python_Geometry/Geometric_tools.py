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
  vertices[0] = [vertices[0][(vertex_idx-idx_min)%len(vertices[0])] for vertex_idx in range(len(vertices[0]))]
  vertices[1] = [vertices[1][(vertex_idx-idx_min)%len(vertices[0])]for vertex_idx in range(len(vertices[0]))]
  
  #rotate
  vertices[0] = [vertices[0][(vertex_idx-irot)%len(vertices[0])]for vertex_idx in range(len(vertices[0]))]
  vertices[1] = [vertices[1][(vertex_idx-irot)%len(vertices[0])]for vertex_idx in range(len(vertices[0]))]
  
  return vertices




#def STCs_single_Module

#def TCs_single_Module
