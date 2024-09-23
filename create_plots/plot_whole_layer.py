from Python_Geometry.Geometric_tools import *
from create_plots.tools import *
import matplotlib.pyplot as plt

def plot_whole_layer(args):
	Layer = args.Layer

	Module_Vertices = item_list('src/'+args.Modmap_version+'/Modules.json','vertices',Layer)
	Module_UV = item_list('src/'+args.Modmap_version+'/Modules.json','uv',Layer)
	Module_irot = item_list('src/'+args.Modmap_version+'/Modules.json','irot',Layer)
	STC_Vertices = item_list('src/'+args.Modmap_version+'/STCs.json','vertices',Layer)
	STC_indices = item_list('src/'+args.Modmap_version+'/STCs.json','index',Layer)

	plt.figure(figsize = (18,18))
	plt.title(label =  'Layer '+str(Layer))
	plt.xlabel('x (mm)')
	plt.ylabel('y (mm)')
	
	for STC_idx in range(len(STC_Vertices)):
		vertices = STC_Vertices[STC_idx]
		Xvertices= vertices[0] +[vertices[0][0]]
		Yvertices= vertices[1] +[vertices[1][0]]
		#plt.plot(Xvertices,Yvertices,color = "red")
		x,y = np.sum(np.array(vertices[0]))/len(vertices[0]),np.sum(np.array(vertices[1]))/len(vertices[0])
		#plt.annotate(str(STC_indices[STC_idx]),(x-20,y-10),size =  '5')
		
	for module_idx in range(len(Module_Vertices)):
		vertices = Module_Vertices[module_idx]
		Xvertices= vertices[0] +[vertices[0][0]]
		Yvertices= vertices[1] +[vertices[1][0]]
		plt.plot(Xvertices,Yvertices,color = "black")
		
		x,y = np.sum(np.array(vertices[0]))/len(vertices[0]),np.sum(np.array(vertices[1]))/len(vertices[0])
		if args.UV == "yes":
	    		u,v = Module_UV[module_idx][0],Module_UV[module_idx][1]
	    		#plt.annotate("("+str(u)+","+str(u)+")",(x-60,y-10),size =  '16') #Pedro coordinates
	    		plt.annotate("("+str(v-u)+","+str(v)+")",(x-60,y-10),size =  '12') #CMSSW coordinates

		if args.irot == "yes":
	    		plt.annotate(str(irot),(x-60,y-10),size =  '12')
	for module_idx in range(len(Module_Vertices)):
		vertices = one_sector_rotation(Module_Vertices[module_idx])
		Xvertices= vertices[0] +[vertices[0][0]]
		Yvertices= vertices[1] +[vertices[1][0]]
		plt.plot(Xvertices,Yvertices,color = "black")
		
		x,y = np.sum(np.array(vertices[0]))/len(vertices[0]),np.sum(np.array(vertices[1]))/len(vertices[0])
		if args.UV == "yes":
	    		u,v = Module_UV[module_idx][0],Module_UV[module_idx][1]
	    		#plt.annotate("("+str(u)+","+str(u)+")",(x-60,y-10),size =  '16') #Pedro coordinates
	    		plt.annotate("("+str(u)+","+str(u-v)+")",(x-60,y-10),size =  '12') #CMSSW coordinates
		if args.irot == "yes":
	    		plt.annotate(str(irot),(x-60,y-10),size =  '12')

	for module_idx in range(len(Module_Vertices)):
		vertices = one_sector_rotation(Module_Vertices[module_idx])
		Xvertices= vertices[0] +[vertices[0][0]]
		Yvertices= vertices[1] +[vertices[1][0]]
		plt.plot(Xvertices,Yvertices,color = "black")
		
		x,y = np.sum(np.array(vertices[0]))/len(vertices[0]),np.sum(np.array(vertices[1]))/len(vertices[0])
		if args.UV == "yes":
	    		u,v = Module_UV[module_idx][0],Module_UV[module_idx][1]
	    		#plt.annotate("("+str(u)+","+str(u)+")",(x-60,y-10),size =  '16') #Pedro coordinates
	    		plt.annotate("("+str(-u)+","+str(-v)+")",(x-60,y-10),size =  '12') #CMSSW coordinates
		if args.irot == "yes":
	    		plt.annotate(str(irot),(x-60,y-10),size =  '12')

	plt.savefig('test')
	
	
