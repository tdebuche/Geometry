import json
from collections import defaultdict

with open("Python_Geometry/src/Modules.json",'r') as file:
  Modules = json.load(file)

HDorLD = defaultdict(list)
for layer in range(len(Modules)):
  for module_idx in range(len(Modules[layer])):
    module = Modules[layer][module_idx]
    res = (module["TCcount"] == "12")
    HDorLD[(layer+1,module["u"],module["v"])].append(res)

def get_HDorLD(Layer,module_u,module_v):
  if HDorLD[(Layer,module_u,module_v)] != [] :
    if HDorLD[(Layer,module_u,module_v)][0] :
      return('HD')
  return('LD')

def get_STC_index(HDorLD,cell_u,cell_v):
  #LD
  if HDorLD == 'LD':
    if (cell_u <= cell_v) and (cell_u < 8):
      return 0
    if (cell_v > 7) and (cell_u >= 8):
      return 1
    if (cell_u > cell_v) and (cell_v <= 7):
      return 2
  #HD
  if HDorLD == 'HD':
    if (cell_v-cell_u >= 6) and (cell_u <= 5):
      return 0
    if (cell_v-cell_u >= 6) and (cell_u <= 11) and (cell_u > 5):
      return 1
    if (cell_v-cell_u >= 0) and (cell_v-cell_u < 6) and  (cell_u <= 11) and (cell_u > 5):
      return 2
    if (cell_v-cell_u >= 0) and (cell_v-cell_u < 6) and  (cell_u <= 5):
      return 3
    if (cell_v > 17) and  (cell_u > 17):
      return 4
    if (cell_v > 11) and (cell_v <= 17) and (cell_u > 17):
      return 5
    if (cell_v > 11) and (cell_v <= 17) and (cell_u > 11) and (cell_u <= 17):
      return 6
    if  (cell_v > 17) and (cell_u > 11) and (cell_u <= 17):
      return 7
    if (cell_v-cell_u < -6) and (cell_v <= 5):
      return 8
    if (cell_v-cell_u < 0) and (cell_v-cell_u >= -6) and (cell_v <= 5):
      return 9
    if (cell_v-cell_u < 0) and (cell_v-cell_u >= -6) and (cell_v <= 11) and (cell_v > 5):
      return 10
    if (cell_v-cell_u < -6) and (cell_v <= 11) and (cell_v > 5):
      return 11

def get_STC_index_from_TC(HDorLD,cell_u,cell_v):
  #LD
  if HDorLD == 'LD':
    if (cell_u <= cell_v) and (cell_u <= 3):
      return 0
    if (cell_v >= 4) and (cell_u >= 4):
      return 1
    if (cell_u > cell_v) and (cell_v <= 3):
      return 2
  if HDorLD == 'HD':
    if (cell_v-cell_u >= 2) and (cell_u <= 1):
      return 0
    if (cell_v-cell_u >= 2) and (cell_u <= 3) and (cell_u > 1):
      return 1
    if (cell_v-cell_u >= 0) and (cell_v-cell_u < 2) and  (cell_u <= 3) and (cell_u > 1):
      return 2
    if (cell_v-cell_u >= 0) and (cell_v-cell_u < 2) and  (cell_u <= 1):
      return 3
    if (cell_v > 5) and  (cell_u > 5):
      return 4
    if (cell_v > 3) and (cell_v <= 5) and (cell_u > 5):
      return 5
    if (cell_v > 3) and (cell_v <= 5) and (cell_u > 3) and (cell_u <= 5):
      return 6
    if  (cell_v > 5) and (cell_u > 3) and (cell_u <= 5):
      return 7
    if (cell_v-cell_u <= -3) and (cell_v <= 1):
      return 8
    if (cell_v-cell_u < 0) and (cell_v-cell_u >= -2) and (cell_v <= 1):
      return 9
    if (cell_v-cell_u < 0) and (cell_v-cell_u >= -2) and (cell_v <= 3) and (cell_v > 1):
      return 10
    if (cell_v-cell_u < -2) and (cell_v <= 3) and (cell_v > 1):
      return 11
  print((HDorLD,cell_u,cell_v))
