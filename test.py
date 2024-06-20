from TSVtoXML.Geometry import TsvToXML
import json
from Python_Geometry.XMLtoModules import read_xml

SrcFile = "TSVtoXML/src/v15.5/geometry_sipmontile.hgcal.txt"

#GeometryFile = TsvToXML( SrcFile , "Geometry.xml" )


read_xml("Geometry.xml" )

