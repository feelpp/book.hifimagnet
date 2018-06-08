#!/bin/bash

module load singularity

usage(){
   echo ""
   echo "Description:"
   echo "               Run salome within Singularity image"
   echo ""
   echo "Usage:"
   echo "               script.sh [ <option> ] ... ]"
   echo ""
   echo "Options:"
   echo ""
   echo "-t             Activate Salome TUI mode"
   echo "-s             Specify python script to be used (only valid when TUI is on)"
   echo "-a             Specifiy parameters of the python script (only valid in combination with -s, optional)"
   echo "-i             Change singularity image (default: feelpp_salome-mso4sc.simg)"
   echo "-r             Change singularity image directory (default: $LUSTRE/singularity_images)"
   echo "-l             Specify directory holding MeshGems license key (default: $STORE/Distene)"
   echo "-d             Activate debug mode"
   echo ""
   exit 1
}

DEBUG=0


#########################################################
## parse parameters
##########################################################
while getopts "hts:a:i:d" option ; do
   case $option in
       h ) usage ;;
       t ) TUI=1 ;;
       s ) SCRIPT=$OPTARG ;;
       a ) SCRIPT_ARGS=$OPTARG ;;
       i ) IMAGE=$OPTARG ;;
       r ) SINGULARITY_DIR=$OPTARG ;;
       l ) KEYDIR=$OPTARG ;;
       d ) DEBUG=1 ;;
       ? ) usage ;;
   esac
done
# shift to have the good number of other args
shift $((OPTIND - 1))

# Optionally set VERSION and others if none is defined. 
: ${IMAGE=feelpp_salome-mso4sc.simg}
: ${TUI=0}
: ${SCRIPT=""}
: ${SCRIPT_ARGS=""}
: ${KEYDIR=$STORE/Distene}

: ${SINGULARITY_DIR=$LUSTRE/singularity_images}

if [ $TUI = "1" ]; then

    if [ -z $SCRIPT ]; then
	echo "Trying to run salome in TUI mode without a script"
	echo "you need to define a python script"
	usage
    fi

    if [ -z $SCRIPT_ARGS ]; then
	singularity exec --nv \
	    -H $HOME:/home/$USER \
	    -B /mnt \
	    -B /scratch \
	    -B $KEYDIR:/opt/DISTENE/DLim \
	    $SINGULARITY_DIR/$IMAGE \
	    salome -t $SCRIPT
    else
	singularity exec --nv \
	    -H $HOME:/home/$USER \
	    -B /mnt \
	    -B /scratch \
	    -B $STORE/Distene:/opt/DISTENE/DLim \
	    $SINGULARITY_DIR/$IMAGE \
	    salome -t $SCRIPT args:$SCRIPT_ARGS
    fi 
else
    singularity exec --nv \
	-H $HOME:/home/$USER \
	-B /mnt \
	-B /scratch \
	-B $STORE/Distene:/opt/DISTENE/DLim \
	$SINGULARITY_DIR/$IMAGE \
	vglrun salome 
fi
