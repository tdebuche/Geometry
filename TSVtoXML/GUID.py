
def Header( endcap , sector , subsector , subsystem ):
  if endcap & ~0x1 : raise Exception( "Invalid endcap" )
  if sector & ~0x3 : raise Exception( "Invalid sector" )
  if subsector & ~0x1 : raise Exception( "Invalid subsector" )
  if subsystem & ~0x3 : raise Exception( "Invalid subsystem" )

  return ( ( endcap & 0x1 ) << 31 ) | \
         ( ( sector & 0x3 ) << 29 ) | \
         ( ( subsector & 0x1 ) << 28 ) | \
         ( ( subsystem & 0x3 ) << 26 )

def ObjectType( object_type ):
  return ( ( object_type & 0xF ) << 22 )

def ResetObjectType( word ):
    return word & ~( 0xF << 22 )

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def get_endcap( id ):
  return ( id >> 31 ) & 0x1

def get_sector( id ):
  return ( id >> 29 ) & 0x3

def get_subsector( id ):
  return ( id >> 28 ) & 0x1

def get_subsystem( id ):
  return ( id >> 26 ) & 0x3

def get_object_type( id ):
  return ( id >> 22 ) & 0xF

def get_type_str( id ):
  subsystem , type = get_subsystem( id ) , get_object_type( id )
  if subsystem==0:
    if type == 14: return "Tileboard"
    if type == 15: return "Scintillator Module"
    if type == 0: return "Silicon Module"
    if type == 1: return "Trigger Cell"
    if type == 2: return "Motherboard"
    if type == 3: return "Trigger lpGBT"
    if type == 4: return "DAQ lpGBT"
    if type == 5: return "Region"
    if type == 6: return "Patch"
  if subsystem==1:	
    if type == 0: return "S1"
    if type == 1: return "S1 input channel"
    if type == 2: return "S1 output channel"
    if type == 3: return "Backend fibre"
    if type == 4: return "Backend cluster channel"
    if type == 5: return "Backend tower channel"
  if subsystem==2:	
    if type == 0: return "S2"
    if type == 1: return "S2 input channel"
    if type == 2: return "S2 output channel"
    
  raise Exception( "Bad Type" )
  
  
def add_sector_to_id( id , sector ):
 return ( id & ~( 0x3 << 29 ) ) | ( ( sector & 0x3 ) << 29 ) 
  
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def silicon_module_id ( plane , u , v , endcap = 0 , sector = 3 , subsector = 0 ):
  if plane & ~0x3F : raise Exception( "Invalid plane" )
  if u & ~0xF : raise Exception( "Invalid u" )
  if v & ~0xF : raise Exception( "Invalid v" )
  return Header( endcap , sector , subsector , 0 ) | ObjectType( 0 ) | ( ( plane & 0x3F ) << 16 ) | ( ( u & 0xF ) << 12 ) | ( ( v & 0xF ) << 8 )

def tileboard_id ( plane , u , v , endcap = 0 , sector = 3 , subsector = 0 ):
  if plane & ~0x3F : raise Exception( "Invalid plane" )
  if u & ~0xF : raise Exception( "Invalid u" )
  if v & ~0xF : raise Exception( "Invalid v" )
  return Header( endcap , sector , subsector , 0 ) | ObjectType( 14 ) | ( ( plane & 0x3F ) << 16 ) | ( ( u & 0xF ) << 12 ) | ( ( v & 0xF ) << 8 )

def scintillator_module_id ( plane , u , v , endcap = 0 , sector = 3 , subsector = 0 ):
  if plane & ~0x3F : raise Exception( "Invalid plane" )
  if u & ~0xF : raise Exception( "Invalid u" )
  if v & ~0xF : raise Exception( "Invalid v" )
  return Header( endcap , sector , subsector , 0 ) | ObjectType( 15 ) | ( ( plane & 0x3F ) << 16 ) | ( ( u & 0xF ) << 12 ) | ( ( v & 0xF ) << 8 )

def trigger_cell_id ( plane , u , v , cell_u , cell_v , endcap = 0 , sector = 3 , subsector = 0 ):
  if cell_u & ~0xF : raise Exception( "Invalid cell_u" )
  if cell_v & ~0xF : raise Exception( "Invalid cell_v" )
  return silicon_module_id( plane , u , v , endcap , sector , subsector ) | ObjectType( 1 ) | ( ( cell_u & 0xF ) << 4 ) | ( ( cell_v & 0xF ) << 0 ) # No need to reset object type as Module_id object_type is 0

def motherboard_id ( plane , mbid , endcap = 0 , sector = 3 , subsector = 0 ):
  if plane & ~0x3F : raise Exception( "Invalid plane" )
  if mbid & ~0x1FFF : raise Exception( "Invalid mbid" )
  return Header( endcap , sector , subsector , 0 ) | ObjectType( 2 ) | ( ( plane & 0x3F ) << 16 ) | ( ( mbid & 0x1FFF ) << 3 )

def trigger_lpGBT_id ( plane , mbid , index , endcap = 0 , sector = 3 , subsector = 0 ):
  if index & ~0x7 : raise Exception( "Invalid index" )
  return ResetObjectType( motherboard_id( plane , mbid , endcap , sector , subsector ) ) | ObjectType( 3 ) | ( ( index & 0x7 ) << 0 )

def daq_lpGBT_id ( plane , mbid , index , endcap = 0 , sector = 3 , subsector = 0 ):
  if index & ~0x7 : raise Exception( "Invalid index" )
  return ResetObjectType( motherboard_id( plane , mbid , endcap , sector , subsector ) ) | ObjectType( 4 ) | ( ( index & 0x7 ) << 0 )

def region_id ( plane , type , index , endcap = 0 , sector = 3 , subsector = 0 ):
  if plane & ~0x3F : raise Exception( "Invalid plane" )
  if type & ~0x3 : raise Exception( "Invalid type" )
  if index & ~0x1 : raise Exception( "Invalid index" )
  return Header( endcap , sector , subsector , 0 ) | ObjectType( 5 ) | ( ( plane & 0x3F ) << 16 ) | ( ( type & 0x3 ) << 1 ) | ( ( index & 0x1 ) << 0 )

def patch_id ( is_trigger , layer , ID0 , ID1 , ID2 , endcap = 0 , sector = 3 , subsector = 0 , subid = 0x3F ):
  if is_trigger & ~0x1 : raise Exception( "Invalid trigger/daq flag" )
  if layer & ~0x1 : raise Exception( "Invalid layer" )
  if ID0 & ~0x7F : raise Exception( "Invalid ID0" )
  if ID1 & ~0x7F : raise Exception( "Invalid ID1" )
  if ID2 & ~0x3 : raise Exception( "Invalid ID2" )
  return Header( endcap , sector , subsector , 0 ) | ObjectType( 6 )| ( ( subid & 0x3F ) << 16 ) | ( ( is_trigger & 0x1 ) << 15 ) | ( ( layer & 0x1 ) << 14 ) | ( ( ID0 & 0x7F ) << 8 ) | ( ( ID1 & 0x7F ) << 2 ) | ( ( ID2 & 0x3 ) << 0 )  



def get_plane( id ):
  if get_subsystem( id ) != 0 : raise Exception( "get_planes can only be used in subsystem 0" )
  return ( id >> 16 ) & 0x3F

def get_module_uv ( id ):
  if get_subsystem( id ) != 0 : raise Exception( "get_module_uv can only be used in subsystem 0" )
  if get_object_type( id ) != 0 and get_object_type( id ) != 15 : raise Exception( "get_module_uv can only be used on module-IDs" ) 
  return ( id >> 12 ) & 0xF , ( id >> 8 ) & 0xF

def get_motherboard_id( id ):
  if get_subsystem( id ) != 0 : raise Exception( "get_motherboard_id can only be used in subsystem 0" )
  if get_object_type( id ) < 2 or get_object_type( id ) > 3 : raise Exception( "get_motherboard_id can only be used on motherboard-IDs" ) 
  return ( id >> 3 ) & 0x1FFF

def get_region_type( id ):
  if get_subsystem( id ) != 0 : raise Exception( "get_region_type can only be used in subsystem 0" )
  if get_object_type( id ) < 5 : raise Exception( "get_region_type can only be used on region-IDs" ) 
  return ( id >> 1 ) & 0x3

def get_region_id( id ):
  if get_subsystem( id ) != 0 : raise Exception( "get_region_id can only be used in subsystem 0" )
  if get_object_type( id ) < 5 : raise Exception( "get_region_id can only be used on region-IDs" ) 
  return ( id >> 0 ) & 0x1


def get_patch_is_trigger( id ):
  if get_subsystem( id ) != 0 : raise Exception( "get_patch_is_trigger can only be used in subsystem 0" )
  if get_object_type( id ) != 6 : raise Exception( "get_patch_is_trigger can only be used on patch-IDs" ) 
  return ( id >> 15 ) & 0x1

def get_patch_layer( id ):
  if get_subsystem( id ) != 0 : raise Exception( "get_patch_is_trigger can only be used in subsystem 0" )
  if get_object_type( id ) != 6 : raise Exception( "get_patch_is_trigger can only be used on patch-IDs" ) 
  return ( id >> 14 ) & 0x1

def get_patch_id( id ):
  if get_subsystem( id ) != 0 : raise Exception( "get_patch_id can only be used in subsystem 0" )
  if get_object_type( id ) != 6 : raise Exception( "get_patch_id can only be used on patch-IDs" ) 
  return ( ( id >> 8  ) & 0x7F ) , ( ( id >> 2 ) & 0x7F ) , ( ( id >> 0 ) & 0x3 )


# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def S1_id( s1index , endcap = 0 , sector = 3 , subsector = 0 ):
  if s1index & ~0x3f : raise Exception( "Invalid index" )
  return Header( endcap , sector , subsector , 1 ) | ObjectType( 0 ) | ( ( s1index & 0x3F ) << 16 )

def S1_input_channel_id( s1index , index , endcap = 0 , sector = 3 , subsector = 0 ):
  if index & ~0x7F : raise Exception( "Invalid index" )
  return S1_id( s1index , endcap , sector , subsector ) | ObjectType( 1 ) | ( ( index & 0x7F ) << 0 ) # No need to reset object type as S1_id object_type is 0

def Add_input_channel_to_S1id( s1id , index ):
  if index & ~0x7F : raise Exception( "Invalid index" )
  return s1id | ObjectType( 1 ) | ( ( index & 0x7F ) << 0 ) # No need to reset object type as S1_id object_type is 0

def S1_output_channel_id( s1index , index , endcap = 0 , sector = 3 , subsector = 0 ):
  if index & ~0x7F : raise Exception( "Invalid index" )
  return S1_id( s1index , endcap , sector , subsector ) | ObjectType( 2 ) | ( ( index & 0x7F ) << 0 ) # No need to reset object type as S1_id object_type is 0

def Add_output_channel_to_S1id( s1id , index ):
  if index & ~0x7F : raise Exception( "Invalid index" )
  return s1id | ObjectType( 2 ) | ( ( index & 0x7F ) << 0 ) # No need to reset object type as S1_id object_type is 0

def S1_backend_fibre_id( s1index , tmindex , fibre , endcap = 0 , sector = 3 , subsector = 0 ):
  if tmindex & ~0x1F : raise Exception( "Invalid tmindex" )
  if fibre & ~0x7 : raise Exception( "Invalid fibre" )
  return S1_id( s1index , endcap , sector , subsector ) | ObjectType( 3 ) | ( ( tmindex & 0x1F ) << 11 ) | ( ( fibre & 0x7 ) << 8 ) # No need to reset object type as S1_id object_type is 0

def Add_backend_fibre_to_S1id( s1id , tmindex , fibre ):
  if tmindex & ~0x1F : raise Exception( "Invalid tmindex" )
  if fibre & ~0x7 : raise Exception( "Invalid fibre" )
  return s1id | ObjectType( 3 ) | ( ( tmindex & 0x1F ) << 11 ) | ( ( fibre & 0x7 ) << 8 ) # No need to reset object type as S1_id object_type is 0

def S1_backend_cluster_channel_id( s1index , tmindex , fibre , channel , endcap = 0 , sector = 3 , subsector = 0 ):
  if channel & ~0x3 : raise Exception( "Invalid channel" )
  return ResetObjectType( S1_backend_fibre_id( s1index , tmindex , fibre , endcap , sector , subsector ) ) | ObjectType( 4 ) | ( ( channel & 0x3 ) << 6 )

def Add_backend_cluster_channel_to_S1id( s1id , tmindex , fibre , channel ):
  if fibre & ~0x7 : raise Exception( "Invalid fibre" )
  if channel & ~0x3 : raise Exception( "Invalid channel" )
  return s1id | ObjectType( 4 ) | ( ( tmindex & 0x1F ) << 11 ) | ( ( fibre & 0x7 ) << 8 ) | ( ( channel & 0x3 ) << 6 ) # No need to reset object type as S1_id object_type is 0

# def S1_backend_cluster_frame_id( s1index , tmindex , fibre , channel , frame , endcap = 0 , sector = 3 , subsector = 0 ):
  # return ResetObjectType( S1_backend_cluster_channel_id( s1index , tmindex , fibre , channel , endcap , sector , subsector ) ) | ObjectType( 5 ) | ( ( frame & 0x7F ) << 0 )

# def Add_backend_cluster_frame_to_S1id( s1id , tmindex , fibre , channel , frame ):
  # return s1id | ObjectType( 5 ) | ( ( tmindex & 0x1F ) << 11 ) | ( ( fibre & 0x3 ) << 9 ) | ( ( channel & 0x3 ) << 7 ) | ( ( frame & 0x7F ) << 0 ) # No need to reset object type as S1_id object_type is 0

# def S1_backend_tower_channel_id( s1index , tmindex , fibre , channel , endcap = 0 , sector = 3 , subsector = 0 ):
  # return ResetObjectType( S1_backend_fibre_id( s1index , tmindex , fibre , endcap , sector , subsector ) ) | ObjectType( 5 ) | ( ( channel & 0x3 ) << 6 )

# def S1_backend_tower_frame_id( s1index , tmindex , fibre , channel , frame , endcap = 0 , sector = 3 , subsector = 0 ):
  # return ResetObjectType( S1_backend_tower_channel_id( s1index , tmindex , fibre , channel , endcap , sector , subsector ) ) | ObjectType( 7 ) | ( ( frame & 0x7F ) << 0 )

def get_s1index( id ):
  if get_subsystem( id ) != 1 : raise Exception( "get_s1index can only be used in subsystem 1" )
  return ( id >> 16 ) & 0x3F

def get_backend_fibre( id ):
  if get_subsystem( id ) != 1 : raise Exception( "get_backend_fibre can only be used in subsystem 1" )
  if get_object_type( id ) < 3 : raise Exception( "get_backend_fibre can only be used on region-IDs" )   
  return ( id >> 8 ) & 0x7
  
def get_backend_channel( id ):
  if get_subsystem( id ) != 1 : raise Exception( "get_backend_channel can only be used in subsystem 1" )
  if get_object_type( id ) < 4 : raise Exception( "get_backend_channel can only be used on region-IDs" )   
  return ( id >> 6 ) & 0x3
  
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def S2_id( tmindex , endcap = 0 , sector = 3 ):
  if tmindex & ~0x1F : raise Exception( "Invalid tmindex" )
  return Header( endcap , sector , 0 , 2 ) | ObjectType( 0 ) | ( ( tmindex & 0x1F ) << 11 )

def S2_input_channel_id( tmindex , index , endcap = 0 , sector = 3 ):
  if index & ~0x7F : raise Exception( "Invalid index" )
  return S2_id( tmindex , endcap , sector ) | ObjectType( 1 ) | ( ( index & 0x7F ) << 0 ) # No need to reset object type as S2_id object_type is 0

def Add_input_channel_to_S2id( s2id , index ):
  if index & ~0x7F : raise Exception( "Invalid index" )
  return s2id | ObjectType( 1 ) | ( ( index & 0x7F ) << 0 ) # No need to reset object type as S2_id object_type is 0

def S2_output_channel_id( tmindex , index , endcap = 0 , sector = 3 ):
  if index & ~0x7F : raise Exception( "Invalid index" )
  return S2_id( tmindex , endcap , sector ) | ObjectType( 2 ) | ( ( index & 0x7F ) << 0 ) # No need to reset object type as S2_id object_type is 0

def Add_output_channel_to_S2id( s2id , index ):
  if index & ~0x7F : raise Exception( "Invalid index" )
  return s2id | ObjectType( 2 ) | ( ( index & 0x7F ) << 0 ) # No need to reset object type as S2_id object_type is 0

def get_s2tm( id ):
  if get_subsystem( id ) != 2 : raise Exception( "get_s2tm can only be used in subsystem 2" )
  return ( id >> 11 ) & 0x1F
  
def get_io_index( id ):
  if get_subsystem( id ) == 0 : raise Exception( "get_io_index can only be used on S1 and S2 subsystems" )    
  if get_object_type( id ) != 1 and get_object_type( id ) != 2 : raise Exception( "get_io_index can only be used on S1 or S2 I/O IDs" )   
  return ( id >> 0 ) & 0x7F  
# ---------------------------------------------------------------------------------------------------------------------------------------------------------
