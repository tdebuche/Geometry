import json
from Python_Geometry.Geometric_tools import single_module_STCs


def One_Layer_STCs(modules):
  STCs = []
  for module_idx in range(len(modules)):
    module =  modules[module_idx]
    if module['type']  == "silicon" :
      vertices =  [module['verticesX'],module['verticesY']]
      vertices[0] = vertices[0] + vertices[0][0:6-len(vertices[0])]
      vertices[1] = vertices[1] + vertices[1][0:6-len(vertices[1])]
      module_STCs =  single_module_STCs(vertices,module['irot'],module['TCcount'])
      for STC_idx in range(len(module_STCs)):
        STCs.append({"id": module['id'], "u": module['u'], "v": module['v'],"index": STC_idx, "verticesX": module_STCs[STC_idx][0] , "verticesY": module_STCs[STC_idx][1]})
  STCs = STCs + One_Layer_Scintillator_STCs(modules)
  return(STCs)

def STC_geometry(jsonfile):
  STCs = []
  with open(jsonfile,'r') as file:
    modules = json.load(file)
  for layer in range(47): #true layer is layer +1
    one_layer_modules = modules[layer]
    if layer > 25: 
      STCs.append(One_Layer_STCs(one_layer_modules))
    else :
      STCs.append([])
  with open('Python_Geometry/src/STCs.json', 'w') as file:
    json.dump(STCs, file)
  

def One_Layer_Scintillator_STCs(modules):
  STCs = []
  return(STCs)



#def Layer_with_TCs
