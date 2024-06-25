import json
from TSVtoXML.Geometry import TsvToXML
from Python_Geometry.XMLtoModules import read_xml
from Python_Geometry.Record_Geometry import STC_geometry


SrcFile = "TSVtoXML/src/v15.5/geometry_sipmontile.hgcal.txt"
GeometryFile = TsvToXML( SrcFile , "Geometry.xml" )
read_xml("Geometry.xml" )
STC_geometry("Python_Geometry/src/Modules.json")
