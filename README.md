# Geometry

This repository allows one to produce the geometry files used in the HGCAL_TPG_pTT repository from the "modmaps".

The modmaps can be found here : https://gitlab.cern.ch/hgcal-integration/hgcal_modmap/-/tree/main/geometries.

Basically, this repository allows one to :
- convert the TSV files (modmaps) with module geometry in xml format
- convert the xml module geometry in json files (the ones used by the HGCAL_TPG_pTT repository)
- create the STC geometry from the module geometry and save it in a json file

This repository is splitted in few parts :

- TSVtoXML : convert the TSV files (modmaps) with module geometry in xml format (programs have been taken in a repository of Andrew Rose from Imperial College)
- Python_Geometry : convert the xml module geometry in json files and create/record STCs
- create_plots : create plots to check some items
- plots : store the plots if needed
- src : gather geometry files (modmaps AND xml AND json files)

In each folder, there is a README to present each program.

The program "create_json_geometry" runs every program of this repository for the production of geometry files 
-

This program has one argument which corrresponds to the geometry version. 


The program Display_Layer allows one to create plots of of one layer. There are arguments to choose which items have to be plotted. It is possible to show the Trigger Cells fired by a given particule wirth the argument "event".
