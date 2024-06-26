import json
import argparse
from TSVtoXML.Geometry import TsvToXML
from Python_Geometry.Modules_from_xml import record_modules
from Python_Geometry.create_STCs_from_Modules import record_STCs



parser = argparse.ArgumentParser()
parser.add_argument("--Modmap_version",default = 'v13.1', help="Geometry version")
args = parser.parse_args()

SrcFile = "src/"+args.Modmap_version+"/geometry_sipmontile.hgcal.txt"

TsvToXML( SrcFile , "src/"+args.Modmap_version+"Geometry.xml" )
record_modules(args,"Geometry.xml" )
record_STCs("src/"+args.Modmap_version+"/Modules.json")
