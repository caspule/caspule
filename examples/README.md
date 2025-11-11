This folder contains a ready-to-run examples of CASPULE's system setup pipeline. 

To generate input, data, colvars, and job submission scripts, download one of the folders and run the pipeline with 

```
sh create_InitCoor.sh 
```

**/example_ran** contains all the files you should expect to see after running create_InitCoor.sh

**/example_no_metadynamics** shows an example of how to set up a system without metadynamics biasing

**/change_sticker_pattern_example** shows how you might change the 'seg' parameter in create_InitCoor.sh to create chains with different sticker patternings 

**/change_component_count_example** shows a more advanced example where we add a new chain type, going from A and B type chains to A,B, and C type chains. 

Modify create_InitCoor.sh to create inital conditions with different box sizes, chain counts, chain types, and more!
Extensive documentation is available on our website: [Example system setup guide](https://caspule.github.io/caspule/usage/example_system_setup.html)