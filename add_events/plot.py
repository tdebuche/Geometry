from Python_Geometry.Geometric_tools import *
import matplotlib.pyplot as plt



def plot_TCs_of_multiple_events(args,events):
    event = events[0]
    Layer = args.Layer
    Module_Vertices = item_list('Python_Geometry/src/Modules.json','vertices',Layer)
    STC_Vertices = item_list('Python_Geometry/src/STCs.json','vertices',Layer)
    plt.figure(figsize = (12,8))
    TCs = event[event['good_tc_layer']==layer][0]
    #plt.scatter(TCs['good_tc_x']*10,TCs['good_tc_y']*10)
    modules = Modules[layer-1]
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
        #if TCs[TC_idx]['good_tc_waferu'] :
        if not (u,v) in L:
            L.append((u,v))
        if not getuvsector(layer,u,v):
            print((u,v,layer))
        # else:
            #u,v,sector = getuvsector(layer,u,v)
        plt.annotate('('+str(u)+','+str(v)+')',(TCs['good_tc_x'][TC_idx]*10,TCs['good_tc_y'][TC_idx]*10))
        plt.scatter(TCs['good_tc_x'][TC_idx]*10,TCs['good_tc_y'][TC_idx]*10)
        plt.show()
