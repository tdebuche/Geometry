from Python_Geometry.Geometric_tools import *
from create_plots.tools import get_STC_index_from_TC,create_list_HDorLD,getuvsector
import matplotlib.pyplot as plt

def plot_layer(args):
	Layer = args.Layer

	Module_Vertices = item_list('src/'+args.Modmap_version+'/Modules.json','vertices',Layer)
	Module_UV = item_list('src/'+args.Modmap_version+'/Modules.json','uv',Layer)
	Module_irot = item_list('src/'+args.Modmap_version+'/Modules.json','irot',Layer)
	STC_Vertices = item_list('src/'+args.Modmap_version+'/STCs.json','vertices',Layer)
	STC_indices = item_list('src/'+args.Modmap_version+'/STCs.json','index',Layer)

	plt.figure(figsize = (12,8))
	plt.title(label =  'Layer '+str(Layer))
	plt.xlabel('x (mm)')
	plt.ylabel('y (mm)')
	
	for STC_idx in range(len(STC_Vertices)):
		vertices = STC_Vertices[STC_idx]
		Xvertices= vertices[0] +[vertices[0][0]]
		Yvertices= vertices[1] +[vertices[1][0]]
		plt.plot(Xvertices,Yvertices,color = "red")
		x,y = np.sum(np.array(vertices[0]))/len(vertices[0]),np.sum(np.array(vertices[1]))/len(vertices[0])
		plt.annotate(str(STC_indices[STC_idx]),(x-20,y-10),size =  '5')
		
	for module_idx in range(len(Module_Vertices)):
		vertices = Module_Vertices[module_idx]
		Xvertices= vertices[0] +[vertices[0][0]]
		Yvertices= vertices[1] +[vertices[1][0]]
		plt.plot(Xvertices,Yvertices,color = "black")
		
		x,y = np.sum(np.array(vertices[0]))/len(vertices[0]),np.sum(np.array(vertices[1]))/len(vertices[0])
		if args.UV == "yes":
	    		u,v = Module_UV[module_idx][0],Module_UV[module_idx][1]
	    		plt.annotate("("+str(u)+","+str(v)+")",(x-60,y-10),size =  '8')
		if args.irot == "yes":
	    		plt.annotate(str(irot),(x-60,y-10),size =  '8')

	plt.show()
	
	

def plot_layer_with_events(args,events):
    event = events[0]
    si = event.ds_si
    Layer = args.Layer
    Module_Vertices = item_list('src/'+args.Modmap_version+'/Modules.json','vertices',Layer)
    STC_Vertices = item_list('src/'+args.Modmap_version+'/STCs.json','vertices',Layer)
    plt.figure(figsize = (12,12))
    colors = ['blue','red','green','yellow']
    TCs = si[si['good_tc_layer']==Layer][0]
    HDorLD_list = create_list_HDorLD(args)
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
        u,v,sector = getuvsector(Layer,TCs['good_tc_waferu'][TC_idx],TCs['good_tc_waferv'][TC_idx])
        cell_u,cell_v = TCs['good_tc_cellu'][TC_idx],TCs['good_tc_cellv'][TC_idx]
        HDorLD =  HDorLD_list[(Layer,u,v)][0]
        STC_index = get_STC_index_from_TC(HDorLD,cell_u,cell_v)
        #if TCs[TC_idx]['good_tc_waferu'] :
        plt.annotate('('+str(cell_u)+','+str(cell_v)+')',(TCs['good_tc_x'][TC_idx]*10,TCs['good_tc_y'][TC_idx]*10))
        plt.scatter(TCs['good_tc_x'][TC_idx]*10,TCs['good_tc_y'][TC_idx]*10,color = colors[STC_index%4])
    plt.show()
