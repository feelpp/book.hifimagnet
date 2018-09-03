= To create the geometry:

```
salome -t ${SALOME_HIFIMAGNET}/bin/salome/HIFIMAGNET_Cmd.py args:--cfg=HL-31_H1[_shapes].yaml
```

NB: the executables must be in the path or should be prefixed with appropriate directories.
For instance on Lncmi server:
```
SALOME_VERSION=8.3.0-DB9.5
SALOME_INSTALL_DIR=$HOME/SALOME-${SALOME_VERSION}/INSTALL
SALOME_HIFIMAGNET=${SALOME_INSTALL_DIR}/HIFIMAGNET
PATH=PATH:${SALOME_INSTALL_DIR}/bin/
```

= To create the mesh with Salome and MeshGems :
```
salome -t ${SALOME_HIFIMAGNET}/bin/salome/HIFIMAGNET_Cmd.py args:--helix=HL-31_H1[_shapes].yaml,--mesh
```

= To partition the mesh:
```feelpp_mesh_partitioner --ifile HL-31_H1[_shapes].med  --part 32  --nochdir```

= To run the model (here thermoelectricmodel):
```
mpirun -np 32 feelpp_hfm_thermoelectric_model_3D_V1T1_N1 --config-file HL-31_H1-dble_32_json.cfg
```

NB: the executables must be in the path or should be prefixed with appropriate directories.
For instance on Lncmi server:
```
FEELPP_BUILD_DIR=~trophime/feelpp_build/new_Json
FEELPP_MESH_APPS_DIR=$FEELPP_BUILD_DIR/applications/mesh/
HIFIMAGNET_APPS_DIR=~/feelpp_build/new_Json/research/hifimagnet/applications
```

The thermoelectric model is in ```$HIFIMAGNET_APPS_DIR/ThermoElectricModel/```

= To run the model (here thermoelectricmodel) with singularity :


```
mpirun -np 32 singularity exec \
   -H ${HOME}:/home/${USER} \
   -B ${HOME}/feel:/feel \
   ${HIFIMAGNET_SINGULARITY} \
   feelpp_hfm_thermoelectric_model_3D_V1T1_N1 --config-file HL-31_H1-dble_32_json.cfg
```

For instance on Lncmi stokes server:
```
HIFIMAGNET_SINGULARITY= ${HOME}/singularity_images/hifimagnet-stretch.simg
```

NB: Materials are assumed to be stored in `$cfgdir/../Materials/`. 