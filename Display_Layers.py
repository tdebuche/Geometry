import argparse
from create_plots.plot import provide_events
from create_plots.plot import plot_layer_with_events,plot_layer


parser = argparse.ArgumentParser()



#for the plot
parser.add_argument("Layer", help="Layer to display",type=int)
parser.add_argument("--UV",default = 'no', help="With or without UV")
parser.add_argument("--irot",default = 'no', help="With or without rot")
parser.add_argument("--STCs",default = 'yes', help="With or without STCs")
parser.add_argument("--events",default = 'no', help="With or without events")
#version of the geometry 
parser.add_argument("--Modmap_version",default = 'v13.1', help="Geometry version")
args = parser.parse_args()

if args.events == "yes":
  events = provide_events(1)
  plot_layer_with_events(args,events)

if args.events == "no":
  plot_layer(args)
  
