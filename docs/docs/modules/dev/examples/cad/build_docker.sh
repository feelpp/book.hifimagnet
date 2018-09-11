#! /bin/bash -x

# Some utilities
# !!! NB: contains return 0 for TRUE !!!
contains () {
    local e
    for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
    return 1
}

usage(){
   echo ""
   echo "Description:"
   echo "                 Builds Salome from scratch using Docker"
   echo ""
   echo "Usage:"
   echo "                 build_salome.sh [ <option> ] ... ]"
   echo ""
   echo "Options:"
   echo ""
   echo "-a <app.pyconf>  Specify application config to use (defaut is SALOME-x.y.z_LNCMI_DB)"
   echo ""
   echo "-v <x.y.z>       Specify version to build"
   echo ""
   echo "-p <platform>    Specify the platform to be used (eg buster)"
   echo ""
   echo "-c <compiler>    Specify the compiler to be used (eg gcc, MPI (for openmpi) or Clang)"
   echo ""
   echo "-m               Activate MPI"
   echo ""
   echo "-d               Activate debug (means only start Docker)"
   echo ""
   echo "-u               upload to dockerhub feelpp team"
   echo ""
   echo "-h               Prints this help information"
   echo ""
   exit 1
}

UPLOAD=0
DEBUG=0
MPI=0
BROWSER=firefox

# List of Ubuntu suites. Update these when needed.
UBUNTU_SUITES=("bionic" "artful" "zesty" "yakkety" "xenial")

# List of Debian suites.
DEBIAN_SUITES=( "buster" "stretch" "wheezy" "jessie" )
DEBIAN_TESTING="buster"

#########################################################
## parse parameters
##########################################################
while getopts "hdv:p:mc:a:u" option ; do
   case $option in
       h ) usage ;;
       a ) APPLICATION=$OPTARG ;;
       v ) VERSION=$OPTARG ;;
       d ) DEBUG=1 ;;
       p ) PLATFORM=$OPTARG ;;
       m ) MPI=1 ;;
       c ) COMPILER=$OPTARG ;;
       d ) UPLOAD=1 ;;
      ? ) usage ;;
   esac
done
# shift to have the good number of other args
shift $((OPTIND - 1))

if [ "$DEBUG" = "1" ]; then
    set -x
fi

# Optionally set VERSION and others if none is defined. 
: ${VERSION:="8.2.0"}
: ${PLATFORM:="buster"}
: ${COMPILER:="gcc"}

# Set Qt version depending on Salome major
: ${QTVER:="qt5"}
MAJOR=$(echo $VERSION | cut -d. -f1)
if [ "$MAJOR" = "7" ]; then
    QTVER="qt4"
fi

# Get OS from Platform name

contains $PLATFORM "${UBUNTU_SUITES[@]}"
isUbuntu=$?

contains $PLATFORM "${DEBIAN_SUITES[@]}"
isDebian=$?

if [[ "$isUbuntu" == 1 && "$isDebian" == 1 ]] ; then
	echo "$PLATFORM is unsupported"
	echo "please check your distribution is supported"
	exit 1
fi

cat > lncmi.list <<EOF 
deb http://euler/~trophime/debian/ $PLATFORM main 
deb-src http://euler/~trophime/debian/ $PLATFORM main 
EOF

# Build DOCKERFILE from Dockerfile-salomeTools.in
#       DOCKERTAG set to PLATFORM
#       DOCKERIMAGE set to salome-[MPI-]$VERSION

MPYCONF=$(echo "SALOME-${VERSION}_LNCMI_DB")
MVERSION=$(echo "${VERSION}")
if [ "$MPI" = "1" ]; then
    MPYCONF=$(echo "SALOME-${VERSION}-MPI_LNCMI_DB")
    MVERSION=$(echo "${VERSION}-mpi")
    COMPILER="MPI"
    echo "WARNING: Force use of openmpi compiler"
fi

# set application
: ${APPLICATION:="${MPYCONF}"}
if [ ! -f PROJECT/applications/$APPLICATION.pyconf ]; then
    echo "PROJECT/applications/$APPLICATION.pyconf: no such file"
    exit 1
fi

cp Dockerfile-salomeTools.in Dockerfile-$PLATFORM-salomeTools
perl -pi -e "s|MVERSION|${MVERSION}|g" Dockerfile-$PLATFORM-salomeTools
perl -pi -e "s|VERSION|${VERSION}|g" Dockerfile-$PLATFORM-salomeTools
if [ "$isUbuntu" == "0" ]; then
    perl -pi -e "s|OS|ubuntu|" Dockerfile-$PLATFORM-salomeTools
fi
if [ "$isDebian" == "0" ]; then
    BROWSER=$(echo "${BROWSER}-esr")
    perl -pi -e "s|OS|debian|" Dockerfile-$PLATFORM-salomeTools
fi

# for bionic and later: libomnithread4-dev instead of libomnithread3-dev 
: ${OMNITHREAD:="libomnithread3-dev"}
: ${COS:="libcos4-1"}
if [ "$PLATFORM" == "bionic" ]; then
    OMNITHREAD="libomnithread4-dev"
    COS="libcos4-2"
fi

perl -pi -e "s|PLATFORM|${PLATFORM}|" Dockerfile-$PLATFORM-salomeTools
perl -pi -e "s|BROWSER|${BROWSER}|" Dockerfile-$PLATFORM-salomeTools
perl -pi -e "s|OMNITHREAD|${OMNITHREAD}|" Dockerfile-$PLATFORM-salomeTools

DOCKERTAG=$(echo $PLATFORM)
DOCKERIMAGE=$(echo "salome-${MVERSION}")

# Create salome install script
cp salome-install.sh.in salome-${VERSION}.sh
perl -pi -e "s|MPYCONF|${APPLICATION}|" salome-${VERSION}.sh
perl -pi -e "s|COMPILER|${COMPILER}|" salome-${VERSION}.sh
perl -pi -e "s|QTVER|${QTVER}|" salome-${VERSION}.sh

echo "Building Salome ${VERSION} for $DOCKERIMAGE:$DOCKERTAG"

# # Install MeshGems license
# if [ -d /opt/DISTENE ]; then
#     cp /opt/DISTENE/DLim/dlim8.var.*sh .
#     cp /opt/DISTENE/DLim/dlim8.key .
# fi

# prior to launch docker check existence of directories
if [ ! -d SALOME-${VERSION}/ARCHIVES ]; then
    echo "SALOME-${VERSION}/ARCHIVES does not exist"
    echo "you should create and populate according to $VERSION [prerequisites] sources"
    exit 1
fi

# should check existence of SALOME_PROFILE_${VER}.tgz

# Create an archive for HIFIMAGNET
pushd ../../salome > /dev/null
tar --exclude-vcs -zcvf HIFIMAGNET.tgz HIFIMAGNET > /dev/null || {
    echo "Failed to create archive for HIFIMAGNET"
    exit 1
}
popd > /dev/null
mv ../../salome/HIFIMAGNET.tgz SALOME-$VERSION/ARCHIVES


if [ ! -d PROJECT ]; then
    echo "PROJECT does not exist"
    exit 1
fi

if [ ! -d salomeTools ]; then
    echo "salomeTools does not exist"
    exit 1
fi

# build Salome env if DOCKER_IMAGE doesn't exist
docker build --build-arg DEBUG=$DEBUG \
       -t $DOCKERIMAGE:$DOCKERTAG \
       -f ./Dockerfile-$PLATFORM-salomeTools .
isOK=$?
if [ "$isOK" != "0" ]; then
    echo "Failed to create $DOCKERIMAGE:$DOCKERTAG with Dockerfile-$PLATFORM-salomeTools"
    exit 1
fi

# build Salome
if [ "$DEBUG" = "1" ]; then
    docker run -ti --rm -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
 	-v $HOME/.Xauthority:/home/feelpp/.Xauthority \
 	--net=host --pid=host --ipc=host  --env QT_X11_NO_MITSHM=1 \
  	-v $HOME/Salome_Packages:/home/feelpp/exports \
  	-v $PWD/SALOME-$VERSION/ARCHIVES:/home/feelpp/salome/ARCHIVES:ro \
  	-v $PWD/PROJECT:/home/feelpp/salome/PROJECT:ro \
  	-v $PWD/salomeTools:/home/feelpp/salome/salomeTools:ro \
  	-v /opt/DISTENE/DLim:/opt/DISTENE/DLim:ro \
 	$DOCKERIMAGE:$DOCKERTAG
else
    docker run -ti --rm -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
 	-v $HOME/.Xauthority:/home/feelpp/.Xauthority \
 	--net=host --pid=host --ipc=host  --env QT_X11_NO_MITSHM=1 \
  	-v $HOME/Salome_Packages:/home/feelpp/exports \
  	-v $PWD/SALOME-$VERSION/ARCHIVES:/home/feelpp/salome/ARCHIVES:ro \
  	-v $PWD//PROJECT:/home/feelpp/salome/PROJECT:ro \
  	-v $PWD/salomeTools:/home/feelpp/salome/salomeTools:ro \
  	-v /opt/DISTENE/DLim:/opt/DISTENE/DLim:ro \
 	$DOCKERIMAGE:$DOCKERTAG  \
    /home/feelpp/salome/salome-$VERSION.sh
    isOK=$?
    
    # clean up
    if [ "$isOK" = "0" ]; then
        rm Dockerfile-$PLATFORM-salomeTools
        rm salome-$VERSION.sh
    else
        exit 1
    fi
fi

# check for Graphics card
if [ -f /usr/bin/lshw ]; then
    GRAPHICS=$(sudo lshw -c video | grep configuration | awk  '{print $2}' | perl -pe 's|driver=||')
    echo "GRAPHICS=$GRAPHICS"
else
    echo "To determine Graphics card install lshw"
fi

# Get Package name
SALOME_PACKAGE=$(basename $(ls -1 -rt $HOME/Salome_Packages/*${VERSION}*.tgz | tail -1))
SALOME_INSTALLDIR=$(echo $SALOME_PACKAGE | tr -d ".tgz")

# create a Dockerfile for running Salome
cp Dockerfile-lncmi.in Dockerfile-${PLATFORM}-${GRAPHICS}
perl -pi -e "s|BROWSER|${BROWSER}|" Dockerfile-${PLATFORM}-${GRAPHICS}
perl -pi -e "s|DOCKERIMAGE|$DOCKERIMAGE|" Dockerfile-${PLATFORM}-${GRAPHICS}
perl -pi -e "s|DOCKERTAG|$DOCKERTAG|" Dockerfile-${PLATFORM}-${GRAPHICS}

cp WELCOME WELCOME-$PLATFORM
perl -pi -e "s|DOCKERIMAGE|$DOCKERIMAGE|" WELCOME-$PLATFORM
perl -pi -e "s|DOCKERTAG|$DOCKERTAG|" WELCOME-$PLATFORM
perl -pi -e "s|GRAPHICS|$GRAPHICS|" WELCOME-$PLATFORM
perl -pi -e "s|VERSION|$VERSION|" WELCOME-$PLATFORM
perl -pi -e "s|DIST|$DIST|" WELCOME-$PLATFORM

perl -pi -e "s|COS|${COS}|" Dockerfile-$PLATFORM-${GRAPHICS}

cp $HOME/Salome_Packages/${SALOME_PACKAGE} .

# --build-arg SALOME_CONFIGPY=${MPYCONF} \

isTesting=0
if [ $DIST = ${DEBIIAN_TESTING} ]; then
   isTesting=1
fi
    
docker build \
       --build-arg DEBUG=$DEBUG \
       --build-arg DIST=$PLATFORM \
       --build-arg isDebian=$isDebian \
       --build-arg isTesting=$isTesting \
       --build-arg GRAPHICS=$GRAPHICS \
       --build-arg SALOME_PACKAGE=${SALOME_PACKAGE} \
       --build-arg SALOME_INSTALLDIR=${SALOME_INSTALLDIR} \
       -t $DOCKERIMAGE:${DOCKERTAG}-${GRAPHICS} \
       -f ./Dockerfile-${PLATFORM}-${GRAPHICS} .
isOK=$?
if [ "$isOK" != "0" ]; then
    echo "Failed to create $DOCKERIMAGE:${DOCKERTAG}-${GRAPHICS} with Dockerfile-${PLATFORM}-${GRAPHICS}"
    exit 1
else
    rm -f ${SALOME_PACKAGE}
    rm -f WELCOME-$PLATFORM
    rm -f Dockerfile-${PLATFORM}-${GRAPHICS}
fi

# clean up docker images
docker rmi $DOCKERIMAGE:$DOCKERTAG

if [ "$DEBUG" = "0" && $Upload = "1" ]; then
    # upload Dockerfile
    if [ -v DOCKER_PASSWORD -a -v DOCKER_LOGIN ]; then
        docker login --username="${DOCKER_LOGIN}" --password="${DOCKER_PASSWORD}";
    else
        echo "Docker environment variable not set: [ DOCKER_PASSWORD , DOCKER_LOGIN ] !"
        exit 1
    fi

    # test if there is already a docker image present
    if [[ "$(docker images -q feelpp/${DOCKERIMAGE}:${DOCKERTAG} 2> /dev/null)" == "" ]]; then
        docker tag ${DOCKERIMAGE}:${DOCKERTAG} feelpp/${DOCKERIMAGE}:${DOCKERTAG}
        docker push feelpp/${DOCKERIMAGE}:${DOCKERTAG}
        docker logout
        
        # remove local images
        IMAGE_ID=$(docker images -q ${DOCKERIMAGE}:${DOCKERTAG} 2> /dev/null)
        docker rmi -f ${IMAGE_ID}

    else
        echo "feelpp/${DOCKERIMAGE}:${DOCKERTAG} already present in local docker images !"
        exit 1
    fi
fi

# generate Singularity

if [ "$DEBUG" = "1" ]; then
    set +x
fi

