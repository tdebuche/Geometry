import numpy as np
import awkward as ak


def item_list(json,item):
  L = []
  with open(json) as file:
    data = json.load(file)[0]
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
    
  
#def STCs_single_Module

#def TCs_single_Module
