from TSVtoXML.Geometry import TsvToXML
import json
from Python_Geometry/XMLtoModules import read_xml

SrcFile = "TSVtoXML/src/v15.5/geometry_sipmontile.hgcal.txt"

#GeometryFile = TsvToXML( SrcFile , "Geometry.xml" )


jsonlist = read_xml("Geometry.xml" )
with open('Python_Geometry/src/Modules.json', 'w') as mon_fichier:
    json.dump(jsonlist, mon_fichier)
