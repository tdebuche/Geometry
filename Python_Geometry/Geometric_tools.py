import numpy as np
import awkward as ak
import json

def item_list(jsonfile,item,layer):
  L = []
  with open(jsonfile,'r') as file:
    data = json.load(file)[layer]
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
