import argparse
from add_events.read_events import provide_events
from add_events.plot import plot_TCs_of_multiple_events


parser = argparse.ArgumentParser()
parser.add_argument("Layer", help="Layer to display",type=int)
parser.add_argument("--UV",default = 'no', help="With or without UV")
parser.add_argument("--irot",default = 'no', help="With or without rot")
parser.add_argument("--STCs",default = 'no', help="With or without STCs")
parser.add_argument("--Record",default = 'no', help="Record all layers")
args = parser.parse_args()


events = provide_events(1)
plot_TCs_of_multiple_events(args,events)
