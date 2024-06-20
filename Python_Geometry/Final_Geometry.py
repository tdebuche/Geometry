import json
from Python_Geometry.Geometric_tools import single_module_STCs
from Python_Geometry.Geometric_tools import single_tileboard_STCs



def One_Layer_STCs(layer,modules):
  STCs = []
  for module_idx in range(len(modules)):
    module =  modules[module_idx]
    
    if module['type']  == "silicon" :
      vertices =  [module['verticesX'],module['verticesY']]
      vertices[0] = vertices[0] + vertices[0][0:6-len(vertices[0])]
      vertices[1] = vertices[1] + vertices[1][0:6-len(vertices[1])]
      module_STCs =  single_module_STCs(vertices,module['irot'],module['TCcount'])
      for STC_idx in range(len(module_STCs)):
        STCs.append({"id": module['id'],"type": 'silicon', "u": module['u'], "v": module['v'],"index": STC_idx, "verticesX": module_STCs[STC_idx][0] , "verticesY": module_STCs[STC_idx][1]})
        
    if module['type']  == "scintillator" :
      vertices =  [module['verticesX'],module['verticesY']]
      tileboard_STCs =  single_tileboard_STCs(layer,vertices,module['u'],module['TCcount'])
      for STC_idx in range(len(tileboard_STCs)):
        STCs.append({"id": module['id'], "type": 'scintillator',"u": module['u'], "v": module['v'],"index": STC_idx, "verticesX": tileboard_STCs[STC_idx][0] , "verticesY": tileboard_STCs[STC_idx][1]})
      
  return(STCs)

def STC_geometry(jsonfile):
  STCs = []
  with open(jsonfile,'r') as file:
    modules = json.load(file)
  for layer in range(47): #true layer is layer +1
    one_layer_modules = modules[layer]
    if layer > 25: 
      STCs.append(One_Layer_STCs(layer+1,one_layer_modules))
    else :
      STCs.append([])
  with open('Python_Geometry/src/STCs.json', 'w') as file:
    json.dump(STCs, file)


#def Layer_with_TCs
