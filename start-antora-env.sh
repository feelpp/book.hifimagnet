#!/bin/bash

USER_ID=${LOCAL_USER_ID:-999}

if [ $USER_iD != "999"]; then
    echo "Starting with UID : $USER_ID"
    useradd -m -s /bin/bash -d /home/user -u $USER_ID -G video,docker user
    export HOME=/home/user

    # Define alias
    cat << EOF > $HOME/.bash_aliases
     alias cp='cp -i'
     echo "alias egrep='egrep --color=auto'
     alias fgrep='fgrep --color=auto'
     alias grep='grep --color=auto'
     alias ls='ls --color=auto'
     alias mv='mv -i'
     alias rm='rm -i'    
    EOF
fi

bash

