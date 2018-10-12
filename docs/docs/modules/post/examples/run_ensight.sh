#!/bin/bash

module load singularity

usage(){
   echo ""
   echo "Description:"
   echo "               Run Ensight within Singularity image"
   echo ""
   echo "Usage:"
   echo "               script.sh [ <option> ] ... ]"
   echo ""
   echo "Options:"
   echo ""
   echo "-t             Activate Ensight Batch mode"
   echo "-s             Specify python script to be used (only valid when TUI is on)"
   echo "-a             Specifiy parameters of the python script (only valid in combination with -s, optional)"
   echo "-l             Specifiy directory holding license file"
   echo "-d             Activate debug mode"
   echo ""
   exit 1
}

DEBUG=0

#########################################################
## parse parameters
##########################################################
while getopts "hts:a:l:d" option ; do
   case $option in
       h ) usage ;;
       t ) TUI=1 ;;
       s ) SCRIPT=$OPTARG ;;
       a ) SCRIPT_ARGS=$OPTARG ;;
       l ) KEYDIR=$OPTARG ;;
       d ) DEBUG=1 ;;
       ? ) usage ;;
   esac
done
# shift to have the good number of other args
shift $((OPTIND - 1))

# Optionally set VERSION and others if none is defined. 
: ${TUI=0}
: ${SCRIPT=""}
: ${SCRIPT_ARGS=""}
: ${KEYDIR=$STORE/Ensight}

if [ ! -z ${SREGISTRY_STORAGE} ]; then
    echo "SREGISTRY_STORAGE not defined"
    echo "please setup SREGISTRY_STORAGE to point to your local sregistry repository"
    echo "ex: export SREGISTRY_STORAGE=$LUSTRE/singularity_images"
    exit 1
fi
   
if [ $TUI = "1" ]; then
    if [ -z $SCRIPT ]; then
	echo "Trying to run Ensiight in BATCH in TUI mode without a script"
	echo "you need to define either a ensight or python script"
	usage
    fi
else
singularity exec --nv \
  -H ${HOME}:/home/$USER \
  -B /scratch \
  -B /mnt \
  -B $KEYDIR:/opt/licenses \
  $SREGISTRY_STORAGE/singularity_images/ensight-10.2.3c.simg \
  vglrun ensight102
fi
