import json
import argparse
from TSVtoXML.Geometry import TsvToXML
from Python_Geometry.XMLtoModules import read_xml
from Python_Geometry.create_STCs_from_Modules import record_STCs



parser = argparse.ArgumentParser()
parser.add_argument("--Modmap_version",default = 'v13.1', help="Geometry version")
args = parser.parse_args()

SrcFile = "src/"+args.Modmap_version+"/geometry_sipmontile.hgcal.txt"

TsvToXML( SrcFile , "src/"+args.Modmap_version+"Geometry.xml" )
read_xml(args,"Geometry.xml" )
record_STCs("src/"+args.Modmap_version+"/Modules.json")
