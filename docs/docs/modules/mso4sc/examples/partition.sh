#! /bin/bash
set -x

usage(){
   echo ""
   echo "Description:"
   echo "               Laod a cfg file and Partition Mesh "
   echo ""
   echo "Usage:"
   echo "               partition.sh -i cfg -n parts [force]]"
   echo ""
   echo "Options:"
   echo "-i <cfgfile>   Specify the input file"
   echo "-n <parts>     Number of partitions"
   echo "-f             Force the partitionning of the mesh"
   echo "-h             Prints this help information"
   echo ""
}

#########################################################
## parse parameters
##########################################################
while getopts "hi:n:f" option ; do
   case $option in
       h ) usage ;;
       i ) INPUT=$OPTARG ;;
       n ) PARTS=$OPTARG ;;
       f ) FORCE=true ;;
       ? ) usage ;;
   esac
done
# shift to have the good number of other args
shift $((OPTIND - 1))

: ${INPUT:="None"}
: ${PARTS:=1}
: ${FORCE:=false}

# echo "INPUT=$INPUT"
# echo "PARTS=$PARTS"
# echo "FORCE=$FORCE"

if [ ! -f ./"$INPUT" ] || [ "$INPUT" = "None" ]; then
    echo "no input file found: $INPUT"
    echo "usage: partition INPUT [PARTS] [false|true]"
    exit 1
fi

if [ "$PARTS" -eq 1 ]; then
    echo "skip partition as PARTS=$PARTS"
    exit 0
fi

FILEMSH=$(grep "geofile=" $INPUT |  cut -d "=" -f2)
echo "FILEMSH=$FILEMSH"

PMESH=$(echo $FILEMSH | cut -d "." -f1)
EXT=$(echo $FILEMSH | cut -d "." -f2)
echo "PMESH=$PMESH"
echo "EXT=$EXT"

if [ "$EXT" = "geo" ] ||  [ "$EXT" = "msh" ] ||  [ "$EXT" = "med" ]; then
    exit 0
fi

# check if json file is already partitioned with PARTS
if [ "$EXT" = "json" ]; then
    N=$(egrep "\"n\":" ${FILEMSH} |  cut -d ":" -f2 | tr -d '[:space:]' | tr -d '\"')
    echo "N=$N"
    if [ $N -eq $PARTS ]; then
	echo "${FIELMSH} already partitionned with $PARTS"
        if  [ ! $FORCE ]; then
	    exit 0
	else
	    echo "Force partition with $PARTS"
	fi
    fi

    # MSH serial
    MESH=$(echo $PMESH | perl -pe "s|_p||g")
    echo "Looking for $MESH"
    if [ -f $MESH.msh ]; then
	echo "Original Mesh: $MESH.msh"
	MESH=$(echo $MESH.msh) 
    elif [ -f $MESH.med ]; then
	echo "Original Mesh: $MESH.med"
	gmsh -3 -bin $MESH.med -o $MESH.msh
	status=$?
	if [ "$status" != "0" ]; then
	    echo "Fail to convert $MESH.med into $MESH.msh"
	    exit 1
	fi
	MESH=$(echo $MESH.msh) 
    else
	echo "No Original Mesh found (.msh or .med supported)"
	exit 1
    fi
fi


echo "feelpp_mesh_partitioner --gmsh.scale=0.001 --ifile ${MESH}.msh --ofile ${PMESH} --part ${PARTS}"
feelpp_mesh_partitioner --gmsh.scale=0.001 --ifile ${MESH} --ofile ${PMESH} --part ${PARTS}
status=$?

if [ "$status" != "0" ]; then
    echo "feelpp_mesh_partitioner --gmsh.scale=0.001 --ifile ${MESH} --ofile ${PMESH} --part ${PARTS}: FAILS (status=$status)"
    echo "see partition.log for details"
    exit 1
fi
