from collections import defaultdict
import numpy as np
import awkward as ak
import uproot
import math

class EventData():
    def __init__(self, ds_si, ds_sci, gen):
        self.ds_si  = ds_si
        self.ds_sci  = ds_sci
        self.ds_stc = None


    
def provide_event(ev, gen):
    ev['r_over_z'] = np.sqrt(ev.good_tc_x**2 + ev.good_tc_y**2)/ev.good_tc_z
    ev['MB_v'] = np.floor((ev.good_tc_cellv-1)/4)
    #ev = ev[[x for x in ak.fields(ev) if not x in ["good_tc_x","good_tc_y","good_tc_z"]]]
    
    # dividing silicon and scintillators
    sci = ev[ev['good_tc_subdet'] == 10]
    si  = ev[ev['good_tc_subdet'] != 10]
    
    # selecting first 120 sector only
    sci = sci[sci['good_tc_cellv']<=48]
    #si = si[si['good_tc_layer'] < 27]

  
    return EventData(si, sci,gen)



def provide_events(n):
    base_path = '/eos/home-m/mchiusi/s2_emulator/'
    name_tree = 'l1tHGCalTriggerNtuplizer/HGCalTriggerNtuple'
    filepath  = base_path + 'DoublePhoton_FlatPt-1To100_PU200_Phase2Fall22DRMiniAOD_24-05-02_emulator_realbcstc_v2-v1.root'

    branches_tc = [
        'good_tc_x', 'good_tc_y', 'good_tc_z',
        'good_tc_phi', 'good_tc_layer', 'good_tc_cellu','good_tc_cellv',
        'good_tc_waferu', 'good_tc_waferv',
        'good_tc_pt', 'good_tc_subdet'
    ]

    branches_gen = [
        'event', 'good_genpart_exeta', 'good_genpart_exphi', 'good_genpart_energy'
    ]

    tree = uproot.open(filepath)[name_tree]
    events_ds = []
    for ev in range(n):
      data = tree.arrays(branches_tc, entry_start=ev, entry_stop=ev+1, library='ak')
      data_gen = tree.arrays(branches_gen, entry_start=ev, entry_stop=ev+1, library='ak')[0]
      events_ds.append(provide_event(data, data_gen))
    return events_ds
