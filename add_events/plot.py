from Python_Geometry.Geometric_tools import *
from add_events.tools import get_STC_index_from_TC,get_HDorLD
import matplotlib.pyplot as plt



def plot_TCs_of_multiple_events(args,events):
    event = events[0]
    si = event.ds_si
    Layer = args.Layer
    Module_Vertices = item_list('Python_Geometry/src/Modules.json','vertices',Layer)
    STC_Vertices = item_list('Python_Geometry/src/STCs.json','vertices',Layer)
    plt.figure(figsize = (12,12))
    colors = ['blue','red','green','yellow']
    TCs = si[si['good_tc_layer']==Layer][0]
    for STC_idx in range(len(STC_Vertices)):
	    vertices = STC_Vertices[STC_idx]
	    Xvertices= vertices[0] +[vertices[0][0]]
	    Yvertices= vertices[1] +[vertices[1][0]]
	    plt.plot(Xvertices,Yvertices,color = "red")
    for module_idx in range(len(Module_Vertices)):
        vertices = Module_Vertices[module_idx]
        Xvertices= vertices[0] +[vertices[0][0]]
        Yvertices= vertices[1] +[vertices[1][0]]
        plt.plot(Xvertices,Yvertices,color = "black")
    for TC_idx in range(len(TCs['good_tc_layer'])):
        u,v = TCs['good_tc_waferu'][TC_idx],TCs['good_tc_waferv'][TC_idx]
        cell_u,cell_v = TCs['good_tc_cellu'][TC_idx],TCs['good_tc_cellv'][TC_idx]
        HDorLD =  get_HDorLD(Layer,u,v)
        STC_index = get_STC_index_from_TC(HDorLD,cell_u,cell_v)
        #if TCs[TC_idx]['good_tc_waferu'] :
        plt.annotate('('+str(cell_u)+','+str(cell_v)+')',(TCs['good_tc_x'][TC_idx]*10,TCs['good_tc_y'][TC_idx]*10))
        plt.scatter(TCs['good_tc_x'][TC_idx]*10,TCs['good_tc_y'][TC_idx]*10,color = colors[STC_index%4])
    plt.show()
