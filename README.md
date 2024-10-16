# Geometry

This recovery allows one to produce the geometry files used in the HGCAL_TPG_pTT repository from the "modmaps".

The modmaps can be found here : https://gitlab.cern.ch/hgcal-integration/hgcal_modmap/-/tree/main/geometries.

Basically, this repository allows one to :
- convert the TSV files (modmaps) with module geometry in xml format
- convert the xml module geometry in json files (the ones used by the HGCAL_TPG_pTT repository)
- create the STC geometry from the module geometry and save it in a json file

This recovery is splitted in few parts :

- TSVtoXML : convert the TSV files (modmaps) with module geometry in xml format (programms have been taken in a repository of Andrew Rose from Imperial College)
- Python_Geometry : convert the xml module geometry in json files
- create_plots : create some plots to check some items
- plots : record the needed plots here
- src : gather geometry files (modmaps AND xml AND json files)
