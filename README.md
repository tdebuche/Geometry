# Geometry

This recovery allows one to produce the geometry files used in the HGCAL_TPG_pTT repository from the "modmaps".

The modmaps can be found here : https://gitlab.cern.ch/hgcal-integration/hgcal_modmap/-/tree/main/geometries.

Basically, this repository allows one to :
- convert the TSV files (modmaps) with module geometry in a xml format
- convert the xml module geometry in json files (the ones used by the HGCAL_TPG_pTT repository)
- create the STC geometry from the module geometry and save it in a json file

