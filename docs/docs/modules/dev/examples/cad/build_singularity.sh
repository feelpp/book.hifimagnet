#! /bin/bash -x

usage(){
   echo ""
   echo "Description:"
   echo "               Builds Salome Singularity container from official release "
   echo ""
   echo "Usage:"
   echo "               build.sh [ <option> ] ... ]"
   echo ""
   echo "Options:"
   echo ""
   echo "-i <dockerimage> Specify the name of docker image. Default is hifimagnet-from-scratch"
   echo ""
   echo "-t <tag>         Specify tag to use"
   echo ""
   echo "-b <bootstrap.def> Specify the name of bootstrap.def file. Default is hifimagnet-docker.def"
   echo ""
   echo "-h              Prints this help information"
   echo ""
   exit 1
}

TESTSUITE=0

#########################################################
## parse parameters
##########################################################
while getopts "hb:t:i:s:u:p:" option ; do
   case $option in
       h ) usage ;;
       b ) BOOTSTRAP=$OPTARG ;;
       t ) DOCKERTAG=$OPTARG ;;
       i ) DOCKERIMAGE=$OPTARG ;;
       s ) TESTSUITE=1 ;;
       u ) DOCKER_USER=$OPTARG ;;
       p ) DOCKER_PASSWD=$OPTARG ;;       
       ? ) usage ;;
   esac
done
# shift to have the good number of other args
shift $((OPTIND - 1))

# Optionally set VERSION and others if none is defined. 
: ${RELEASE:="yakkety"}
: ${BOOTSTRAP:="hifimagnet-docker.def"}
: ${DOCKERFILE="Dockerfile"}
: ${BRANCH:="develop"}
: ${DOCKERTAG=${BRANCH}-${RELEASE}}
: ${DOCKERIMAGE="hifimagnet"}

: ${DOCKER_USER=${DOCKER_LOGIN}}
: ${DOCKER_PASSWD=${DOCKER_PASSWORD}}

if [ -f  hifimagnet-${DOCKERTAG}.simg ]; then
    echo "hifimagnet-${DOCKERTAG}.simg already exists"
    exit 1
fi

# Check dockerhub credential
if [ ! -z ${DOCKER_USER} ] && [ ! -z ${DOCKER_PASSWD} ] ; then
    docker login --username=${DOCKER_USER} --password="${DOCKER_PASSWD}"
    isOK=$?
    if [ "$isOK" != "0" ]; then
        echo "credentials for dockerhub are invalid"
        echo "username=${DOCKER_USER}"
        echo "password=${DOCKER_PASSWD}"
        exit 1
    fi
else
    echo "Docker environment variable not set: [ DOCKER_PASSWORD , DOCKER_LOGIN ] !"
    exit 1
fi

# Set credentials for singularity
export SINGULARITY_DOCKER_USERNAME=${DOCKER_USER}
export SINGULARITY_DOCKER_PASSWORD=${DOCKER_PASSWD}

# Check existence of docker image
# if [[ "$(docker images -q feelpp/${DOCKERIMAGE}:${DOCKERTAG} 2> /dev/null)" == "" ]]; then
#     docker pull feelpp/${DOCKERIMAGE}:${DOCKERTAG}
# fi

# TODO:
# Get Release from Dockerfile: requires lbs-release to be installed
# Set Os to Release in BOOSTRAP file or Check Os/Release are consistent

# Get singularity version
SINGULARITY_BIN=$(which singularity)

SINGULARITY_MAJOR_VERSION=`${SINGULARITY_BIN} --version | sed 's/\([0-9]*\)[.]*[0-9]*[.]*[0-9]*.*/\1/'`
SINGULARITY_MINOR_VERSION=`${SINGULARITY_BIN} --version | sed 's/[0-9]*[.]*\([0-9]*\)[.]*[0-9]*.*/\1/'`
SINGULARITY_PATCH_VERSION=`${SINGULARITY_BIN} --version | sed 's/[0-9]*[.]*[0-9]*[.]*\([0-9]*\).*/\1/'`

# Get image size if singularity is less than 2.4
if [ $SINGULARITY_MAJOR_VERSION -eq 2 ] && [ $SINGULARITY_MINOR_VERSION -le 3 ] ; then
    SAFETY=1.1
    SIZE_MB=""
    SIZE=$(docker images feelpp/${DOCKERIMAGE}:${DOCKERTAG}  --format "{{.Size}}")
    isGB=$(echo $SIZE | grep GB)
    if [ -n "$isGB" ] ; then
        SIZE=$(echo $SIZE | tr -d "GB")
        echo "feelpp/${DOCKERIMAGE}:${DOCKERTAG}: ${SIZE} GB"
        SIZE_MB=$(echo "(${SAFETY}*${SIZE}*1024+0.5)/1" | bc)
    else
        isMB=$(echo $SIZE | grep GB)
        if [ -n "$isMB" ] ; then
            SIZE_MB=$(echo "(${SAFETY}*${SIZE}+0.5)/1" | bc)
            echo "feelpp/${DOCKERIMAGE}:${DOCKERTAG}: ${SIZE_MB}"
        fi
    fi

    ${SINGULARITY_BIN} create --size ${SIZE_MB} ${DOCKERIMAGE}-${DOCKERTAG}.simg
    ${SINGULARITY_BIN} -vvv import ${DOCKERIMAGE}-${DOCKERTAG}.simg docker://feelpp/${DOCKERIMAGE}:${DOCKERTAG}

    # NB user should be a sudoer at least for singularity
    # sudo -E ${SINGULARITY_BIN} -vvv  bootstrap ${DOCKERIMAGE}-${DOCKERTAG}.img ${BOOTSTRAP}

else
    # echo "singularity 2.4 and above are not supported right now"
    # exit 1

    # NB user should be a sudoer at least for singularity
    sudo -E ${SINGULARITY_BIN} -vvv build --force --notest --writable "./${DOCKERIMAGE}-${DOCKERTAG}.simg" "./${BOOTSTRAP}"

    # add option -w to have a "compatible" singularity image
fi

# where to store Singularity images??

# clear singularity cache ??
rm -rf $HOME/.singularity
#sudo rm -rf /root/.singularity???

docker logout
