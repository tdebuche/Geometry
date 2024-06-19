import xml.etree.cElementTree as ET
import hashlib, os, datetime
from Hgc import GUID
from math import ceil

# ===========================================================================================================================================================================  
class NonXmlDocument:

  def __init__( self , TargetFilename , sources=[] , verbose = True ):
    self.TargetFilename = TargetFilename    
    self.manifest = f"{os.path.dirname( os.path.abspath( TargetFilename ) )}/.manifest"    
    self.root = None
    self.node = None
    self.sources = sources
    self.verbose = verbose
 
  def __enter__( self ): 

    if not os.path.isfile( self.manifest ): 
      if self.verbose: print( f"NonXmlDocument: Manifest file for '{self.TargetFilename}' does not exist - regenerating" )
      self.root = ET.Element( "manifest" )    
      return False  
    
    self.root = ET.parse( self.manifest ).getroot()

    if not os.path.isfile( self.TargetFilename ): 
      if self.verbose: print( f"NonXmlDocument: File '{self.TargetFilename}' does not exist - generating" )
      return False

    self.node = self.root.find( f'./file[@name="{self.TargetFilename}"]' )

    if self.node is None: 
      if self.verbose: print( f"NonXmlDocument: No manifest entry for file '{self.TargetFilename}' - regenerating" )
      return False  
    
    Srcs = XmlCheckSrcHashes( self.node.attrib[ "Srcs" ] )
    if Srcs is None:
      if self.verbose: print( f"NonXmlDocument: Source check for file '{self.TargetFilename}' failed - regenerating" )
      return False      
    
    if sorted( self.sources ) != sorted( Srcs ):
      if self.verbose: print( f"NonXmlDocument: Source list for file '{self.TargetFilename}' failed - regenerating" )
      return False 
    
    if self.verbose: print( f"NonXmlDocument: File '{self.TargetFilename}' exists; its sources exist and the source-hashes match - not regenerating" )
    self.root = None
    return True
    
    
  def __exit__(self, exc_type, exc_val, exc_tb):
    if exc_type: return
    if self.root is None: return    
    
    if self.node is None: ET.SubElement( self.root , "file" , attrib={ "name":self.TargetFilename , "Srcs":XmlMakeSrcHashes( self.sources ) } ) 
    else:                 self.node.attrib[ "Srcs" ] = XmlMakeSrcHashes( self.sources )

    tree = ET.ElementTree( self.root )
    ET.indent( tree , space="\t" , level=0 )
    tree.write( self.manifest )    
# ===========================================================================================================================================================================  




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

# ==================================================================================================================================================================
def GeometryAuxFile( root , Srcs , ZeroOutDaq = False ):
  """
  Unpack the HGC GeometryAux XML file
  <p/> aFilename - The name of the XML file
  """
  
  Top = OpenFile( Srcs[0] , ZeroOutDaq = ZeroOutDaq )  

  for plane in root:
    Plane = Top.Planes [ int( plane.attrib[ "href" ] , 10 ) ]
    for motherboard in plane:      
      Motherboard = Plane.Motherboards[ int( motherboard.attrib[ "href" ] , 16 ) ]
      for module in motherboard:     
        Module = Motherboard.Modules[ int( module.attrib[ "href" ] , 16 ) ]
        setattr( Module  , "Areas" , { int(y[0]) : float(y[1]) for y in [ x.split(":") for x in module.attrib[ "Areas" ].split( ";" ) ] } )
               
  return Top
# ==================================================================================================================================================================

# ==================================================================================================================================================================
def GeometryAux2File( root , Srcs , ZeroOutDaq = False ):
  """
  Unpack the HGC GeometryAux XML file
  <p/> aFilename - The name of the XML file
  """
  
  Top = OpenFile( Srcs[0] , ZeroOutDaq = ZeroOutDaq )  
  
  setattr( Top , "TCunits" , {} )

  for plane in root:
    Plane = Top.Planes [ int( plane.attrib[ "href" ] , 10 ) ]
    for motherboard in plane:      
      Motherboard = Plane.Motherboards[ int( motherboard.attrib[ "href" ] , 16 ) ]
      for module in motherboard:     
        Module = Motherboard.Modules[ int( module.attrib[ "href" ] , 16 ) ]
        Triangles = [ ( tuple(int(z) for z in y[0].split(",")) , int( y[1] ) , float( y[2] ) ) for y in [ x.split(":") for x in module.attrib[ "Triangles" ].split( ";" ) ] ]
        setattr( Module  , "Triangles" , { x[0]:x[2] for x in Triangles } )
        
        for uvw,i,_ in Triangles:
          if not uvw in Top.TCunits: Top.TCunits[uvw] = i
          elif Top.TCunits[uvw] != i : raise Exception( "TCunit mismatch" )
            
  return Top
# ==================================================================================================================================================================



# ==================================================================================================================================================================
def TcGeometryFile( root , Srcs ):
  """
  Unpack the HGC TcGeometry XML file
  <p/> aFilename - The name of the XML file
  """
  Top = Object()
  setattr( Top , "Planes" , {} )

  for plane in root:
    Plane = Object()
    setattr( Plane , "id"      , int( plane.attrib[ "id" ] , 10 ) )
    setattr( Plane , "Modules" , dict() )
    Top.Planes[ Plane.id ] = Plane

    for module in plane:      
      Module = Object()
      setattr( Module , "id" , int( module.attrib[ "id" ] , 16 ) )
      setattr( Module , "TriggerCells" , dict() )
      
      Plane.Modules[ Module.id ] = Module
    
      for tc in module:     
        TriggerCell = Object()
        setattr( TriggerCell , "id"    , int( tc.attrib[ "id" ] , 16 ) )
        setattr( TriggerCell , "u"     , int( tc.attrib[ "u" ] ) )
        setattr( TriggerCell , "v"     , int( tc.attrib[ "v" ] ) )
        setattr( TriggerCell , "x"     , float( tc.attrib[ "x" ] ) )
        setattr( TriggerCell , "y"     , float( tc.attrib[ "y" ] ) )
        if tc.attrib[ "z" ] != "None" : setattr( TriggerCell , "z"     , float( tc.attrib[ "z" ] ) )
        
        Module.TriggerCells[ TriggerCell.id ] = TriggerCell
               
  return Top
# ==================================================================================================================================================================

# ==================================================================================================================================================================
def PatchFile( root , Srcs , ZeroOutDaq = False ):
  """
  Unpack an HGC Patch-definition XML file
  <p/> aFilename - The name of the XML file
  """
 
  Top = Object()
  setattr( Top , "Patch" , {} )
  
  for subsystem in root:
    Subsystem = []
    Top.Patch[ subsystem.attrib[ "id" ] ] = Subsystem
    
    for pp1 in subsystem:
      PP1 = Object()      
      Subsystem.append( PP1 )
      setattr( PP1 , "type" , "PP1" )
      setattr( PP1 , "id"   , int( pp1.attrib[ "id" ] , 16 ) )
      setattr( PP1 , "rawid"   , pp1.attrib[ "raw-id" ] )
      setattr( PP1 , "connector"   , pp1.attrib[ "type" ] )
      setattr( PP1 , "PP0s" , [] )
      if "group" in pp1.attrib: setattr( PP1 , "group" , int( pp1.attrib[ "group" ] ) )

      for pp0 in pp1:
        PP0 = Object()      
        PP1.PP0s.append( PP0 )
        setattr( PP0 , "type" , "PP0" )
        setattr( PP0 , "id"   , int( pp0.attrib[ "id" ] , 16 ) )
        setattr( PP0 , "rawid"   , pp0.attrib[ "raw-id" ] )
        setattr( PP0 , "connector"   , pp0.attrib[ "type" ] )
        # setattr( PP0 , "Motherboards"  , [ Planes[ GUID.get_plane( MotherboardId ) ].Motherboards[ MotherboardId ] for MotherboardId in [ int( mb.attrib[ "href" ] , 16 ) for mb in pp0 ] ] )
        setattr( PP0 , "Motherboards"  , [ int( mb.attrib[ "href" ] , 16 ) for mb in pp0 ] )
      
  return Top
# ==================================================================================================================================================================

# ==================================================================================================================================================================
def RegionFile( root , Srcs , ZeroOutDaq = False ):
  """
  Unpack an HGC Region-definition XML file
  <p/> aFilename - The name of the XML file
  <p/> ZeroOutDaq - Whether or not to include DAQ rates/links/etc in our model  
  """
  Regions = {}
  
  Top = OpenFile( Srcs[0] , ZeroOutDaq=ZeroOutDaq ) 
  setattr( Top , "Regions" , {} )  
    
  for region in root:
    Region = Object()
    setattr( Region , "type"          , "Region" )    
    setattr( Region , "id"            , int( region.attrib[ "id" ] , 16 ) )
    setattr( Region , "section"       , GUID.get_region_type( Region.id ) ) # Included for consistency with old code, but now extracted from the ID
    setattr( Region , "plane"         , GUID.get_plane( Region.id ) )       # Included for consistency with old code, but now extracted from the ID
    setattr( Region , "ud"            , GUID.get_region_id( Region.id ) )   # Included for consistency with old code, but now extracted from the ID
    setattr( Region , "lr"            , GUID.get_subsector( Region.id ) )   # Included for consistency with old code, but now extracted from the ID    
    setattr( Region , "TriggerLpGbts" , int( region.attrib[ "TriggerLpGbts" ] ) )
    setattr( Region , "TCcount"       , tryInt( region.attrib[ "TCcount" ] ) )
    setattr( Region , "Motherboards"  , [ Top.Planes[ GUID.get_plane( MotherboardId ) ].Motherboards[ MotherboardId ] for MotherboardId in [ int( mb.attrib[ "href" ] , 16 ) for mb in region ] ] )
    Top.Regions[ Region.id ] = Region
    
    if ZeroOutDaq:
      setattr( Region , "DaqLpGbts"     , 0 )
      setattr( Region , "DaqRate"       , 0.0 )
    else:
      setattr( Region , "DaqLpGbts"     , int( region.attrib[ "DaqLpGbts" ] ) )
      setattr( Region , "DaqRate"       , float( region.attrib[ "DaqRate" ] ) )
      
    # Utility fields
    setattr( Region , "ModuleCount"   , 0 )
    setattr( Region , "ModuleCountHO" , 0 )    
    for Motherboard in Region.Motherboards:
      Region.ModuleCount   += Motherboard.ModuleCount
      Region.ModuleCountHO += Motherboard.ModuleCountHO
      setattr( Motherboard , "region" , Region )
        
  return Top
# ==================================================================================================================================================================

# ==================================================================================================================================================================
def S1File( root, Srcs ):
  """
  Unpack an HGC S1-definition XML file
  <p/> aFilename - The name of the XML file
  """

  Top = OpenFile( Srcs[0] , ZeroOutDaq = ( root.attrib[ "SeparateDaq" ] == "True" ) )
  setattr( Top , "S1s" , {} )  
  setattr( Top , "Scenario" , root.attrib[ "id" ] )  
  
  for s1 in root:
    S1 = Object()
    setattr( S1 , "type"     , "S1" )    
    setattr( S1 , "id"       , int( s1.attrib[ "id" ] , 16 ) )
    setattr( S1 , "Regions"  , [ Top.Regions[ RegionId ] for RegionId in [ int( region.attrib[ "href" ] , 16 ) for region in s1 ] ] )
    Top.S1s[ S1.id ] = S1
    
    setattr( S1 , "TriggerLpGbts" , 0 )
    setattr( S1 , "DaqLpGbts"     , 0 )
    setattr( S1 , "DaqRate"       , 0 )
    setattr( S1 , "TCcount"       , 0 )
    setattr( S1 , "ModuleCountHO" , 0 )    
    setattr( S1 , "TriggerModuleCount" , 0 )
    setattr( S1 , "DaqOnlyModuleCount" , 0 )
       
    for Region in S1.Regions:
      S1.TriggerLpGbts += Region.TriggerLpGbts
      S1.DaqLpGbts     += Region.DaqLpGbts
      S1.DaqRate       += Region.DaqRate
      S1.ModuleCountHO += Region.ModuleCountHO      
      if Region.section == 3: S1.DaqOnlyModuleCount += Region.ModuleCount
      else:                   S1.TriggerModuleCount += Region.ModuleCount
      if not Region.TCcount is None : S1.TCcount += Region.TCcount

    # Utility fields
    setattr( S1 , "TriggerFireflies" , int( ceil( S1.TriggerLpGbts / 12.0 ) ) )
    setattr( S1 , "DaqFireflies"     , int( ceil( S1.DaqLpGbts / 12.0 ) ) )
    
  return Top
# ==================================================================================================================================================================

# ==================================================================================================================================================================
def S1ChannelAllocationFile( root, Srcs ):
  """

  """

  Top = OpenFile( Srcs[0] )
  
  for s1 in root: 
    S1 = Top.S1s[ int( s1.attrib[ "id" ] , 16 ) ]

    TCmap = {}

    for channel in s1:  
      ChannelId = int( channel.attrib[ "id" ] , 16 )   
      Fibre , Channel = GUID.get_backend_fibre( ChannelId ) , GUID.get_backend_channel( ChannelId )
      ChannelId = (3*Fibre) + Channel
      # ChannelIdX = int( channel.attrib[ "aux-id" ]  )   
      
      for frame in channel:

        if not "column" in frame.attrib: continue        
        Col , Index = int( frame.attrib[ "column" ] ) , int( frame.attrib[ "index" ] )
        
        FrameId = int( frame.attrib[ "id" ] )
        if not ChannelId in TCmap: TCmap[ ChannelId ] = [ None for i in range( 108 ) ]
                
        if "Motherboard" in frame.attrib:
          MotherboardId = int( frame.attrib[ "Motherboard" ] , 16 )
          for Region in S1.Regions:
            for Motherboard in Region.Motherboards:
              if Motherboard.id == MotherboardId :
                TCmap[ ChannelId ][ FrameId ] = ( Motherboard , Col , Index )
                break
            else: continue
            break

        else:
          ModuleId = int( frame.attrib[ "Module" ] , 16 )
          for Region in S1.Regions:
            for Motherboard in Region.Motherboards:
              for Module in Motherboard.Modules.values():
                if Module.id == ModuleId :
                  TCmap[ ChannelId ][ FrameId ] = ( Module , Col , Index )
                  break
              else: continue
              break
            else: continue
            break

    setattr( S1 , "TCmap" , [ j for i , j in sorted( TCmap.items() ) ] )
    
  return Top
# ==================================================================================================================================================================

# ==================================================================================================================================================================
def BackendMappingFile( root, Srcs ):
  """
  Unpack an HGC S1-to-S2 mapping XML file
  <p/> aFilename - The name of the XML file
  """

  Top = OpenFile( Srcs[0] )
  
  setattr( Top , "BackendMapping" , { 0:{} , 1:{} } )

  for endcap in root: 
    endcapid = int( endcap.attrib[ "id" ] )
    for fibre in endcap:
      fibreid , s1output , s2input , reffibre = int( fibre.attrib[ "id" ] , 16 ) , int( fibre.attrib[ "s1-output" ] , 16 ) , int( fibre.attrib[ "s2-input" ] , 16 ) , int( fibre.attrib[ "ref-fibre" ] , 16 )      
      Top.BackendMapping[ endcapid ][ fibreid ] = ( s1output , s2input , reffibre )
          
  return Top
# ==================================================================================================================================================================

# ==================================================================================================================================================================
def S2ChannelAllocationFile( root, Srcs ):
  """
  """

  Top = OpenFile( Srcs[0] )

  setattr( Top , "S2ChannelAllocation" , {} )
  
  for Col in root: 

    ColId = int( Col.attrib["id"] )
    Top.S2ChannelAllocation[ ColId ] = [ None for i in range( 216 ) ]    
    col = Top.S2ChannelAllocation[ ColId ]

    for Frame in Col:                    
      if "s2-input" in Frame.attrib: 
        FrameId , S1RefChannel , S2Input = int( Frame.attrib["id"] ) , int( Frame.attrib["s1-refchannel"] , 16 ) , int( Frame.attrib["s2-input"] , 16 )
        col[ FrameId ] = ( S1RefChannel , S2Input )
                 
  return Top        
# ==================================================================================================================================================================
      
