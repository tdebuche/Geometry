import xml.etree.cElementTree as ET
import hashlib, os, datetime
from math import ceil




# ===========================================================================================================================================================================  
def md5( filename ):
  hash_md5 = hashlib.md5()
  with open( filename , "rb" ) as f:
    for chunk in iter( lambda: f.read(4096) , b"" ): hash_md5.update( chunk )
  return hash_md5.hexdigest()
# ===========================================================================================================================================================================  

# ===========================================================================================================================================================================  
def XmlMakeSrcHashes( Srcs ):
  return ";".join( [ f"{Src}:{md5( Src )}" for Src in Srcs ] )
# ===========================================================================================================================================================================  

# ===========================================================================================================================================================================  
def XmlCheckSrcHashes( HashStr ):
  xSrcs = []
  
  for pair in HashStr.split( ";" ):    
    if len( pair ) == 0 : continue
    Src , Hash = pair.split( ":" )
    if not os.path.isfile( Src ): return None
    if Hash != md5( Src ): return None
    xSrcs.append( Src )
      
  return xSrcs
# ===========================================================================================================================================================================  

# ===========================================================================================================================================================================  
def XmlCheckBeforeProducing( TargetFilename , Srcs ):
  """
  Check whether the target XML file exists, and if so, whether its source file is consistent with it's hash
  <p/> TargetFilename - The name of the target XML file
  <p/> SrcFilename - The name of the source file for checking consistency
  """
  
  # print( f"Checking '{TargetFilename}'" )
  
  Filepath = os.path.dirname( TargetFilename )

  if len(Filepath) and not os.path.isdir( Filepath ):
    print( f"XmlDocument: File path '{Filepath}' does not exist - creating" )
    os.makedirs( Filepath , exist_ok=True )

  if not os.path.isfile( TargetFilename ):
    print( f"XmlDocument:    File '{TargetFilename}' does not exist - generating" )
    return False
    
  root = ET.parse( TargetFilename ).getroot()
  
  try:
    srcs = root.attrib[ "Srcs" ]
  except:
    print( f"XmlDocument:    File '{TargetFilename}' does not have necessary attributes - regenerating" )
    return False   

  xSrcs = XmlCheckSrcHashes( srcs )

  if xSrcs is None:
    print( f"XmlDocument:    File '{TargetFilename}' exists; but its source-hashes do not match - regenerating" )      
    return False 
  
  if sorted( xSrcs ) != sorted( Srcs ):
    print( f"XmlDocument:    File '{TargetFilename}' exists; but its sources do not match - regenerating" )
    # print( list( sorted( xSrcs ) ) , list( sorted( Srcs ) ) )
    return False 
    
  print( f"XmlDocument:    File '{TargetFilename}' exists; its sources exist and the source-hashes match - not regenerating" )
  return True
# ===========================================================================================================================================================================  

# ===========================================================================================================================================================================  
class XmlDocument:
  """
  Class representing XML document
  """

  def __init__( self , xmlfilename , tag , sources = [] , labels = [] , attribs = {} , skip_check = False ):   
    self.filename = xmlfilename
    self.root = None
    
    if (not skip_check) and XmlCheckBeforeProducing( self.filename , sources ): return      
    self.root = ET.Element( tag , attrib = { "Srcs": XmlMakeSrcHashes( sources ) , "Timestamp":str(datetime.datetime.now()) } )
    for key , value in attribs.items() : self.root.set( key , value )
    for label in labels: self.root.append( ET.Comment( f" {label:200}") )
  
  def __enter__( self ):
    return self.root

  def __exit__(self, exc_type, exc_val, exc_tb):
    if self.root is None: return
    if exc_type: return
    
    tree = ET.ElementTree( self.root )
    ET.indent( tree , space="\t" , level=0 )
    tree.write( self.filename )
# ===========================================================================================================================================================================  



# ===========================================================================================================================================================================  
def OpenFile( aFilename , **aArgs ):
  # print( f"Opening '{aFilename}'" )
  root = ET.parse( aFilename ).getroot()
  
  if "Srcs" in aArgs: raise Exception( f"'Srcs' is not allowed in aArgs" )

  TagToFunction = { "HGC":GeometryFile , "HGC-Aux":GeometryAuxFile , "HGC-Aux2":GeometryAux2File , "HGC-Regions":RegionFile , "HGC-Patch":PatchFile , "HGC-S1":S1File , 
                    "HGC-S1ChannelAllocation":S1ChannelAllocationFile , "HGC-BackendMapping":BackendMappingFile , "HGC-S2ChannelAllocation":S2ChannelAllocationFile ,
                    "HGC-TCgeo": TcGeometryFile }

  if not root.tag in TagToFunction: raise Exception( f"Unknown root tag '{root.tag}' in XML file 'aFilename'" )
  
  Srcs = XmlCheckSrcHashes( root.attrib[ "Srcs" ] )
  if Srcs is None: raise Exception( f"Xml file source-check failed" )
  
  return TagToFunction[ root.tag ]( root , Srcs=Srcs , **aArgs )
# ===========================================================================================================================================================================  



# ==================================================================================================================================================================
"""
New pseudo-datatype for interacting primarily through the XML files
"""
class Object(object):
  """
  Universal HGC Object, be that a module, motherboard, region, plane or S1
  """
  def __init__( self , **attrib ):
    for k , v in attrib.items(): setattr( self , k , v )

  def __repr__( self ): return f"{self.type}(0x{self.id:08X})"

  # def __lt__( self , other ): return self.id < other.id

def tryInt( aStr ):
  """
  Attempt to convert a string to an int, but handle "None" correctly
  """
  if aStr == "None" : return None
  return int( aStr )
# ==================================================================================================================================================================


# ==================================================================================================================================================================
def GeometryFile( root , Srcs , ZeroOutDaq = False ):
  """
  Unpack the HGC Geometry XML file
  <p/> aFilename - The name of the XML file
  <p/> ZeroOutDaq - Whether or not to include DAQ rates/links/etc in our model
  """
  Top = Object()
  setattr( Top , "Planes" , {} )

  for plane in root:
    Plane = Object()
    setattr( Plane , "type"      , "Plane" )
    setattr( Plane , "id"      , int( plane.attrib[ "id" ] , 10 ) )
    setattr( Plane , "Motherboards" , dict() )
    Top.Planes[ Plane.id ] = Plane

    for motherboard in plane:      
      Motherboard = Object()
      setattr( Motherboard , "type"          , "Motherboard" )
      setattr( Motherboard , "id"            , int( motherboard.attrib[ "id" ] , 16 ) )
      setattr( Motherboard , "TriggerLpGbts" , int( motherboard.attrib[ "TriggerLpGbts" ] ) )
      setattr( Motherboard , "TCcount"       , tryInt( motherboard.attrib[ "TCcount" ] ) )
      setattr( Motherboard , "Modules"       , dict() )
      
      if ZeroOutDaq:
        setattr( Motherboard , "DaqLpGbts"     , 0 )
        setattr( Motherboard , "DaqRate"       , 0.0 )
      else:
        setattr( Motherboard , "DaqLpGbts"     , int( motherboard.attrib[ "DaqLpGbts" ] ) )
        setattr( Motherboard , "DaqRate"       , float( motherboard.attrib[ "DaqRate" ] ) )

      # Utility fields
      setattr( Motherboard , "ModuleCount"   , 0 )
      setattr( Motherboard , "ModuleCountHO" , 0 )
      setattr( Motherboard , "Plane"         , Plane )
      
      Plane.Motherboards[ Motherboard.id ] = Motherboard
    
      for module in motherboard:     
        Module = Object()
        setattr( Module , "type"          , "Module" )
        setattr( Module , "id"            , int( module.attrib[ "id" ] , 16 ) )
        if ZeroOutDaq: setattr( Module , "DaqRate"       , 0.0 )
        else:          setattr( Module , "DaqRate"       , float( module.attrib[ "DaqRate" ] ) )
        setattr( Module , "TCcount"       , tryInt( module.attrib[ "TCcount" ] ) )
        setattr( Module , "HighOccupancy" , module.attrib[ "HighOccupancy" ] == "True" )
        setattr( Module , "u"             , int( module.attrib[ "u" ] ) )
        setattr( Module , "v"             , int( module.attrib[ "v" ] ) )
        setattr( Module , "x"             , float( module.attrib[ "x" ] ) )
        setattr( Module , "y"             , float( module.attrib[ "y" ] ) )
        setattr( Module , "Vertices" , [ ( float(y[0]) , float(y[1]) ) for y in [ x.split(",") for x in module.attrib[ "Vertices" ].split( ";" ) ] ] )
        
        if len( list( module ) ):        
          setattr( Module , "TileBoards" , dict() )          
          for tileboard in module:
            Tileboard = Object()
            setattr( Tileboard , "type"          , "Tileboard" )
            setattr( Tileboard , "id"            , int( tileboard.attrib[ "id" ] , 16 ) )
            if ZeroOutDaq: setattr( Tileboard , "DaqRate"       , 0.0 )
            else:          setattr( Tileboard , "DaqRate"       , float( tileboard.attrib[ "DaqRate" ] ) )
            setattr( Tileboard , "TCcount"       , tryInt( tileboard.attrib[ "TCcount" ] ) )
            setattr( Tileboard , "HighOccupancy" , tileboard.attrib[ "HighOccupancy" ] == "True" )
            setattr( Tileboard , "u"             , int( tileboard.attrib[ "u" ] ) )
            setattr( Tileboard , "v"             , int( tileboard.attrib[ "v" ] ) )
            setattr( Tileboard , "x"             , float( tileboard.attrib[ "x" ] ) )
            setattr( Tileboard , "y"             , float( tileboard.attrib[ "y" ] ) )
            setattr( Tileboard , "Vertices" , [ ( float(y[0]) , float(y[1]) ) for y in [ x.split(",") for x in tileboard.attrib[ "Vertices" ].split( ";" ) ] ] )

            Module.TileBoards[ Tileboard.id ] = Tileboard

        setattr( Module , "Motherboard"   , Motherboard )
        Motherboard.Modules[ Module.id ] = Module
        
        Motherboard.ModuleCount += 1
        if Module.HighOccupancy: Motherboard.ModuleCountHO += 1
  
  return Top
# ==================================================================================================================================================================








