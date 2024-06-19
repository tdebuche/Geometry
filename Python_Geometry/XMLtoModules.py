import numpy as np
import awkward as ak
import xml.etree.ElementTree as ET
from collections import defaultdict

import os


def read_xml(file):
    tree = ET.parse(file)
    print(tree)
    root = tree.getroot()
    Modules = [[] for layer in range(47)]
    layer = 0
    for layer_element in root.findall('.//Plane'):
        layer = int(layer_element.get('id'))
        for motherboard_element in layer_element.findall('.//Motherboard'):
            for module_element in motherboard_element.findall('.//Module'):
                int_id = int(module_element.get('id'),16)
                module_id = str(f'{int_id : 08x}')
                u = int(module_element.get('u'))
                v  = int(module_element.get('v'))
                x = float(module_element.get('x'))
                y = float(module_element.get('y'))
		    irot = int(module_element.get('irot'))
                verticesX,verticesY = vertices(module_element.get('Vertices'))
                if Silliciumorscintillateur(int_id) == 'sillicium':
                    Modules[layer-1].append({'id':module_id,'u':u,'v':v,'irot':irot,'verticesX' :verticesX,'verticesY' :verticesY})

    layer = 0
    for layer_element in root.findall('.//Plane'):
        layer = int(layer_element.get('id'))
        for motherboard_element in layer_element.findall('.//Motherboard'):
            for tile_element in motherboard_element.findall('.//TileBoard'):
                int_id = int(tile_element.get('id'),16)
                tile_id = str(f'{int_id : 08x}')
                u = int(tile_element.get('u'))
                v  = int(tile_element.get('v'))
                x = float(tile_element.get('x'))
                y = float(tile_element.get('y'))
		    irot = 999
                verticesX,verticesY = vertices(tile_element.get('Vertices'))
                Modules[layer-1].append({'id':tile_id,'u':u,'v':v,'irot':irot,'verticesX' :verticesX,'verticesY' :verticesY})
    return Modules

def Silliciumorscintillateur(id):
    objtype = (id & 0x03C00000) //(16**5 *4)
    if objtype == 15:
        return('scintillator')
    return('sillicium')
                
def vertices(x):
    X = []
    Y = []
    xcourant = ''
    ycourant = ''
    res = 0 
    for i in range(len(x)):
        if x[i] ==';':
            res = 0
            X.append(float(xcourant))
            Y.append(float(ycourant))
            xcourant = ''
            ycourant = ''
        elif x[i] == ',':
            res = 1
        elif res == 0:
            xcourant += x[i]
        elif res == 1:
            ycourant += x[i]
    X.append(float(xcourant))
    Y.append(float(ycourant))
    return(X,Y)
