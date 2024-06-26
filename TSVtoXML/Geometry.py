from TSVtoXML import GUID
from TSVtoXML.XmlSchema import *
import itertools
import numpy as np

# ===========================================================================================================================================================================  
def TsvToXML( SrcFilename , TargetFilename ):

  ScintillatorTileBoards = { 34:{0:1,1:1} , 
                             35:{2:1,3:1} , # Pedro file weirdness
                             36:{0:1,1:1} , 
                             37:{2:1,3:1} , # Pedro file weirdness
                             38:{0:0,1:1,2:1,3:1} , 
                             39:{0:0,1:1,2:1,3:1} , 
                             40:{0:0,1:1,2:1,3:1} , 
                             41:{0:0,1:1,2:1,3:1} , 
                             42:{0:0,1:1,2:1,3:1} , 
                             43:{0:0,1:1,2:1,3:1} , 
                             44:{0:0,1:0,2:1,3:1,4:1} , 
                             45:{0:0,1:0,2:1,3:1,4:1} , 
                             46:{0:0,1:0,2:1,3:1,4:1} , 
                             47:{0:0,1:0,2:1,3:1,4:1} } 
                       
  ScintillatorTcCounts = { 34:{1:6} , 
                           35:{1:8} , 
                           36:{1:8} , 
                           37:{1:8} , 
                           38:{0:4,1:10} , 
                           39:{0:4,1:12} , 
                           40:{0:6,1:12} , 
                           41:{0:6,1:12} , 
                           42:{0:6,1:12} , 
                           43:{0:6,1:12} , 
                           44:{0:10,1:12} , 
                           45:{0:10,1:12} , 
                           46:{0:10,1:12} , 
                           47:{0:10,1:12} }       

  labels = [ "Hierarchical XML file representing the detector geometry for one 120-degree sector of one endcap based on Pedro's tsv file",
             "Hierarchy is Plane => Motherboard => Silicon Module" ,
             "Hierarchy is Plane => Motherboard => Scintillator Module => Tileboard" ]

  with XmlDocument( TargetFilename , tag="HGC" , labels=labels , sources=[ SrcFilename ] ) as root:
    if root is None: return TargetFilename
    
    Planes , Motherboards , SiModules , ScModules , Tileboards = {} , {} , {} , {} , {}

    # -------------------------------
    with open( SrcFilename , "r" ) as file:
      headers = file.readline().split()  
      for line in file: 
      
        module = Object()
        for header, value in zip( headers , line.split() ) : setattr( module , header , value )
        module.plane , module.MB , module.u , module.v, module.irot = int( module.plane ), int( module.MB ), int( module.u ), int( module.v ), int(float(module.irot))

        # -------------------------------
        # Create the ID and check for errors in Pedro's file
        if module.MB >= 5000:
          setattr( module , "id" , GUID.tileboard_id ( module.plane , module.u , module.v ) )      
          if module.id in Tileboards: raise Exception( f"Tileboard {module.id} already exists : {GUID.get_plane( module.id )} | {GUID.get_module_uv ( module.id )}" )
        else:            
          setattr( module , "id" , GUID.silicon_module_id ( module.plane , module.u , module.v ) )
          if module.id in SiModules: raise Exception( f"Module {module.id} already exists : {GUID.get_plane( module.id )} | {GUID.get_module_uv ( module.id )}" )
        # -------------------------------

        # -------------------------------
        # Output link quantities (rate & links is per-module, fibres is per motherboard)
        module.trigRate , module.trigLinks = float( module.trigRate ) , int( float( module.trigLinks ) )
        setattr( module , "IsHO" , (module.trigLinks > 3) and (module.plane < 27) )
        if not (module.HDorLD == True or module.HDorLD == False):
          module.HDorLD = (module.HDorLD == "1")
        if module.HDorLD:
          setattr( module , "dataRate" ,  float( module.dataRate_hd ) )
          setattr( module , "dataLinks" , int( float( module.dataLinks_hd )) )
        else:
          setattr( module , "dataRate" ,  float( module.dataRate_ld ) )
          setattr( module , "dataLinks" , int( float( module.dataLinks_ld )) )   
          
        #module.engine_trig_fibres ,  module.engine_data_fibres ,  module.engine_ctrl_fibres = int( float( module.engine_trig_fibres ) ) , int( float( module.engine_data_fibres ) ) , int( float( module.engine_ctrl_fibres ) )
        # -------------------------------

        # -------------------------------
        # Fix the module geometry in mirrored layers and in 30-deg rotated layers
        mirror_x = -1 if ( module.plane < 27 ) and ( module.plane % 2 == 0 ) else 1
        setattr( module , "corners" , [ ( mirror_x*float(module.vx_0) , float(module.vy_0) ) , ( mirror_x*float(module.vx_1) , float(module.vy_1) ) , ( mirror_x*float(module.vx_2) , float(module.vy_2) ) , ( mirror_x*float(module.vx_3) , float(module.vy_3) ) , ( mirror_x*float(module.vx_4) , float(module.vy_4) ) , ( mirror_x*float(module.vx_5) , float(module.vy_5) ) , ( mirror_x*float(module.vx_6) , float(module.vy_6) ) ][:int(module.nvertices)] )
        setattr( module , "coords"  , ( mirror_x*float(module.x0) , float(module.y0) ) )
        
        offset120 = 2 * np.pi / 3
        if module.plane == 28 or module.plane == 30 or module.plane == 32:
          offset = np.pi / 6
          x,y = module.coords
          r,phi = ( np.sqrt( x*x + y*y ) , np.arctan2(y,x) )

          if (phi+offset) > offset120: offset -= offset120
          
          module.coords = ( r*np.cos(phi+offset) , r*np.sin(phi+offset) )
          
          rphi_corners = [ ( np.sqrt( x*x + y*y ) , np.arctan2(y,x) ) for (x,y) in module.corners ]
          module.corners = [ ( r*np.cos(phi+offset) , r*np.sin(phi+offset) ) for (r,phi) in rphi_corners ]
        # -------------------------------

        # -------------------------------
        # Set the TC counts
        if module.MB >= 5000:
          setattr( module , "TCcount" ,  None )
        elif module.plane < 27:
          if module.plane < 7 : module.trigLinks= min( 2 , module.trigLinks )    # Max two elinks outside shower max
          elif module.plane < 14 : module.trigLinks= min( 4 , module.trigLinks ) # Max four elinks in shower max
          else : module.trigLinks= min( 2 , module.trigLinks )              # Max two elinks outside shower max
          setattr( module , "TCcount" ,  [ None , 1 , 4 , 6 , 9 , 14 ][ module.trigLinks ] )
        elif module.HDorLD:
          setattr( module , "TCcount" ,  12 )
        else:
          setattr( module , "TCcount" ,  3 )
          
        # -------------------------------

        # -------------------------------
        # Fetch or create the plane element
        if not module.plane in Planes: Planes[ module.plane ] = ET.SubElement( root , "Plane" , attrib={ "id" : f"{module.plane:02}" } )
        plane = Planes[ module.plane ]        
        # -------------------------------

        # -------------------------------
        # Fetch or create the motherboard element
        setattr( module , "mbid" , GUID.motherboard_id( module.plane , module.MB ) )
        if not module.mbid in Motherboards: Motherboards[ module.mbid ] = ET.SubElement( plane , "Motherboard" , attrib={ "id" : f"0x{module.mbid:08X}" , 
                                                                                                                "DaqRate"       : "" ,
                                                                                                                "TCcount"       : "" } )
        #"TriggerLpGbts" : f"{module.engine_trig_fibres}" ,
        #"DaqLpGbts"     : f"{module.engine_data_fibres}" ,
        motherboard = Motherboards[ module.mbid ]
        # -------------------------------

        # -------------------------------
        if module.MB >= 5000:
          ScintillatorModuleU = ScintillatorTileBoards[ module.plane ][ module.u ]
          ScintillatorTcCount = ScintillatorTcCounts[ module.plane ][ ScintillatorModuleU ]
          ScintillatorModuleId = GUID.scintillator_module_id ( module.plane , ScintillatorModuleU , module.v )
          
          if not ScintillatorModuleId in ScModules:
            ScModules[ ScintillatorModuleId ] = ET.SubElement( motherboard , "Module" , attrib={  "id" : f"0x{ScintillatorModuleId:08X}" ,
                                                                                                  "DaqRate"       : f"" , 
                                                                                                  "TCcount"       : f"{ScintillatorTcCount}" ,
                                                                                                  "HighOccupancy" : f"{False}" ,
                                                                                                  "u"             : f"{ScintillatorModuleU}" , 
                                                                                                  "v"             : f"{module.v}" , 
                                                                                                  "x"             : f"" , 
                                                                                                  "y"             : f"" , 
                                                                                                  "Vertices"      : f"" } )

          Module = ScModules[ ScintillatorModuleId ]
                  
          tileboard = ET.SubElement( Module , "TileBoard" , attrib={  "id" : f"0x{module.id:08X}" ,
                                                                      "DaqRate"       : f"{module.dataRate:.3f}" ,
                                                                      "TCcount"       : f"{None}" ,
                                                                      "HighOccupancy" : f"{module.IsHO}" ,
                                                                      "u"             : f"{module.u}" , 
                                                                      "v"             : f"{module.v}" ,
                                                                      "irot"          : f"{module.irot}" ,
                                                                      "x"             : f"{module.coords[0]:.3f}" , 
                                                                      "y"             : f"{module.coords[1]:.3f}" , 
                                                                      "Vertices"      : ";".join( [ f"{X[0]:.3f},{X[1]:.3f}" for X in module.corners ] ) } )
          Tileboards[ module.id ] = tileboard      
        
        else:            
          Module = ET.SubElement( motherboard , "Module" , attrib={ "id" : f"0x{module.id:08X}" ,
                                                                    "DaqRate"       : f"{module.dataRate:.3f}" , 
                                                                    "TCcount"       : f"{module.TCcount}" ,
                                                                    "HighOccupancy" : f"{module.IsHO}" ,
                                                                    "u"             : f"{module.u}" , 
                                                                    "v"             : f"{module.v}" ,
                                                                    "irot"          : f"{module.irot}" ,
                                                                    "x"             : f"{module.coords[0]:.3f}" , 
                                                                    "y"             : f"{module.coords[1]:.3f}" , 
                                                                    "Vertices"      : ";".join( [ f"{X[0]:.3f},{X[1]:.3f}" for X in module.corners ] ) } )
          SiModules[ module.id ] = Module 
        # -------------------------------
    # -------------------------------

    # -------------------------------
    # Finalise sums
    for _ , module in ScModules.items():
      module.attrib[ "DaqRate" ] = f'{ sum( float(x.attrib["DaqRate"] ) for x in module )  :.3f}'
    
      vertices = [ tuple( float(x) for x in vx.split(",") ) for tb in module for vx in tb.attrib[ "Vertices" ].split( ";" ) ]
      rs , phis = [ np.sqrt( x*x + y*y ) for (x,y) in vertices ] , [ np.arctan2( y,x ) for (x,y) in vertices ]
      RMin , RMax , PhiMin , PhiMax = min(rs) , max(rs) , min(phis) , max(phis)

      r, phi = (RMin + RMax)/2 , (PhiMin + PhiMax)/2
      module.attrib[ "x" ] = f"{r*np.cos(phi):.3f}"
      module.attrib[ "y" ] = f"{r*np.sin(phi):.3f}"
      module.attrib[ "Vertices" ] = ";".join( [ f"{r*np.cos(phi):.3f},{r*np.sin(phi):.3f}" for r,phi in [ (RMin , PhiMin) , (RMax , PhiMin) , (RMax , PhiMax) , (RMin , PhiMax) ] ] ) 
    
    
    for _ , motherboard in Motherboards.items():
      motherboard.attrib[ "DaqRate" ] = f'{ sum( float(x.attrib["DaqRate"] ) for x in motherboard ) :.3f}'
      try:    motherboard.attrib[ "TCcount" ] = f'{ sum( int(x.attrib["TCcount"] ) for x in motherboard ) }'
      except: motherboard.attrib[ "TCcount" ] = f"{None}"
    # -------------------------------

    # -------------------------------
    # Sort the entries before exporting
    # root[:] = sorted( root, key=lambda child: child.attrib["id"] )
    for plane in root:
      plane[:] = sorted( plane , key=lambda child: child.get("id") )
      for motherboard in plane:
        motherboard[:] = sorted( motherboard , key=lambda child: child.get("id") )
        for module in motherboard:
          module[:] = sorted( module , key=lambda child: child.get("id") )
    # -------------------------------

  return TargetFilename 
# ===========================================================================================================================================================================  

# # ===========================================================================================================================================================================  
# def Test( Old , New ):

  # if isinstance( Old , Object ) :

    # for x in dir( Old ):
      # if x[0] == '_' :  continue
      # try:  
        # OldChild , NewChild = getattr( Old , x ) , getattr( New , x )      
        # if isinstance( OldChild , Object ) : continue #Skipping 'pointer' to parent
        # Test( OldChild , NewChild )
      # except:
        # print( f"For Attribute {x}" , end=", " )
        # raise
      
  # elif isinstance( Old , dict ) :
    # for ( OldChildId , OldChild ) , ( NewChildId , NewChild ) in zip( sorted( Old.items() ) , sorted( New.items() ) ): 
      # try:
        # Test( OldChild , NewChild )
      # except:
        # print( f"At 0x{OldChildId:08x} 0x{NewChildId:08x}" , end=", " )
        # raise

  # elif isinstance( Old , list ) or isinstance( Old , tuple ) :  
    # for OldChild , NewChild in zip( sorted( Old ) , sorted( New ) ): 
      # try:
        # Test( OldChild , NewChild )
      # except:
        # print( f"At {OldChild} {NewChild}" , end=", " )
        # raise


  # elif isinstance( Old , float ) :
    # if abs( Old - New ) > 0.01:
      # print( f"Value mismatch {Old} {New}" , end=", " )
      # raise Exception
    
  # else:
    # if Old != New:
      # print( f"Value mismatch {Old} {New}" , end=", " )
      # raise Exception
# # ===========================================================================================================================================================================  

# ===========================================================================================================================================================================  
def is_inside( pt , corners ): 
  """
  Utility function to determine if a given x-y point is inside the closed boundary specified by points
  <p/> pt - the x-y point to test
  <p/> corners - list of x-y points specifying the boundary
  """
  
  intersects = 0
  for i in range( len( corners ) ) :
    a , b = corners[i-1] , corners[i]
    x0 , y0 , x1 , y1 = a[0] , a[1] , b[0] , b[1]

    if x1 == x0: continue
    if pt[0] < min( x0 , x1 ) or pt[0] > max( x0 , x1 ): continue

    grad = ( y1 - y0 ) / ( x1 - x0 )
    if ( pt[1] - y0 ) <= ( grad * ( pt[0] - x0 ) ) : intersects += 1
  
    if intersects >= 2: break
   
  return intersects == 1
# ====================================  

# ====================================  
def ProduceAreasXML( SrcFilename ): 
  """
  Write the aux geometry information to an XML file
  <p/> TargetFilename - the name of the XML file
  <p/> Data - The legacy data-structure upon which we calculate and export the aux area information
  <p/> SrcFilename - The name of the geometry XML file associated
  """

  TargetFilename = f"{os.path.splitext( SrcFilename )[0]}.Aux.xml"
  labels = [ "Hierarchical XML file containing the average number of trigger-cells per processing column for one 120-degree sector of one endcap",
             "Hierarchy is Plane => Motherboard => Module" ]
             
  with XmlDocument( TargetFilename , tag="HGC-Aux" , labels=labels , sources=[ SrcFilename ] ) as root:
    if root is None: return TargetFilename

    Top = OpenFile( SrcFilename )
     
    scale = (180/np.pi) * (84/120)

    count , total = 0 , sum( len( Plane.Motherboards ) for Plane in Top.Planes.values() )

    for PlaneId , Plane in sorted( Top.Planes.items() ):
      plane = ET.SubElement( root , "Plane" , attrib={ "href" : f"{PlaneId:02}" } )

      for MotherboardId , Motherboard in sorted( Plane.Motherboards.items() ):
        print( f"{count}/{total}" , end="\r" , flush=True )
        count += 1
       
        motherboard = ET.SubElement( plane , "Motherboard" , attrib={ "href" : f"0x{Motherboard.id:08X}" } )
        
        for _ , Module in Motherboard.Modules.items():
          if Module.TCcount is None: continue

          cols , v = {} , 0          
          xmin , xmax , ymin, ymax = 9e99 , -9e99 , 9e99 , -9e99
          for c in Module.Vertices: xmin , xmax , ymin, ymax = min( xmin , c[0] ) , max( xmax , c[0] ) , min( ymin , c[1] ) , max( ymax , c[1] )
          xmin , xmax , ymin, ymax = int( np.floor( xmin ) ) , int( np.ceil( xmax ) ) , int( np.floor( ymin ) ) , int( np.ceil( ymax ) )

          for x , y  in itertools.product( range( xmin , xmax , 2 ) , range( ymin, ymax , 2 ) ):
            if not is_inside( (x,y) , Module.Vertices ): continue        
            phi = np.arctan2( y , x )          
            col = int( np.floor( phi * scale ) )
            if col in cols: cols[ col ] += 1
            else: cols[ col ] = 1
            v += 1
          
          areas = ";".join( f"{i}:{np.around(j*Module.TCcount/v,2)}" for i,j in sorted( cols.items() ) )
          
          module = ET.SubElement( motherboard , "Module" , attrib={ "href" : f"0x{Module.id:08X}" , "Areas" : areas } )

  return TargetFilename           
# ===========================================================================================================================================================================  






