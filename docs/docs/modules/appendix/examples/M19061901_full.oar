#!/bin/bash            
#OAR -n HL-31 <1>
#OAR -l /nodes=14,walltime=8:00:00 <2>
#OAR -O HL-31_%jobid%.out <3>
#OAR -E HL-31_%jobid%.err
#OAR --project hifimagnet <4>
#OAR --notify mail:youremailadress <5>

# Setup environment <6>
source /applis/site/nix.sh
export NIX_PATH="nixpkgs=$HOME/.nix-defexpr/channels/nixpkgs"
nix-env --switch-profile $NIX_USER_PROFILE_DIR/nur-openmpi4
echo "Load nix-env:" $(nix-env -q)

echo "Singularity:" $(which singularity)
SVERSION=$(singularity --version)
echo "Singularity Version:" ${SVERSION}

nbcores=$(cat $OAR_NODE_FILE|wc -l)
nbnodes=$(cat $OAR_NODE_FILE|sort|uniq|wc -l)
njobs=$(cat $OAR_FILE_NODES | wc -l)

echo "nbcores=" $nbcores
echo "nbnodes=" $nbnodes
echo "np=" $njobs
echo "OAR_WORKDIR=" ${OAR_WORKDIR}

# Exec env (TODO param SVERSION)
IMGS_DIR=/bettik/$USER/singularity <7>
HIFIMAGNET=${IMGS_DIR}/hifimagnet-thermobox-debianpack.sif <8>
if [ ! -f $HIFIMAGNET ]; then
	echo "Cannot find ${HIFIMAGNET}"
fi

# Sim setup <9>
SIMDIR=/bettik/$USER/HL-31
CFG=M19061901-full.cfg
LOG=M19061901-full.log
if [ ! -f $CFG ]; then
	echo "Cannot find ${CFG}"
fi

OUTDIR=${SIMDIR}/full
mkdir -p ${OUTDIR}
echo "create ${OUTDIR}"

# Check if mesh is correctly partitionned: aka nparts==njobs

# Run the program <9>
mpirun -np ${njobs} \
       -machinefile $OAR_NODEFILE \
       -mca plm_rsh_agent "oarsh" -mca btl_openib_allow_ib true \
       --prefix $HOME/.nix-profile \
     singularity exec -H ${OAR_WORKDIR} -B $OUTDIR:/feel $HIFIMAGNET \
       feelpp_hfm_coupledcartmodel_3DP1N1 --config-file ${CFG} 

