#!/usr/bin/env bash
# kumar.mcmillan -at- gmail.com

function usage()
{
    echo "Authorizes a remote host for SSH access"
    echo "by copying your public key to ~/.ssh/authorized_keys ..."
    echo ""
    echo "usage: "`basename $0`" hostname [user]"
    echo ""
}

function cleanup()
{
    if [ -f $TEMP_PUB_KEY_XFER ]
    then
        rm $TEMP_PUB_KEY_XFER
    fi
}

function exit_on_error()
{
    cleanup
    exit 1
}

if [ $# -lt 1 -o "$1" = "-h" -o "$1" = "--help" ]
then
    usage
    exit 0
fi

PUB_KEY=~/.ssh/id_rsa.pub
if [ $# -eq 2 ]; then
    USER=$2
else
    USER=`whoami`
fi
HOST_TO_AUTH=$1
TEMP_PUB_KEY_XFER=/tmp/$USER"_TEMP_KEY"

echo "checking for $PUB_KEY ..."
if [ ! -f $PUB_KEY ]; then
    echo "generating your dsa public key (leave passphrase blank and save to $PUB_KEY when prompted) ..."
    ssh-keygen
    if [ $? -ne 0 ]; then
        echo "ssh-keygen failed"
        exit_on_error
    fi
fi
echo "OK"

cat $PUB_KEY > $TEMP_PUB_KEY_XFER
chmod 700 $TEMP_PUB_KEY_XFER

remote_key=`basename $TEMP_PUB_KEY_XFER`
echo "copying temp pub key to $HOST_TO_AUTH ..."
scp $TEMP_PUB_KEY_XFER $USER@$HOST_TO_AUTH:~/$remote_key
if [ $? -ne 0 ]; then
    echo "scp failed"
    exit_on_error
fi

echo "checking directory structure on remote host ..."
ssh $USER@$HOST_TO_AUTH <<'END'
if [ ! `ls -a1 ~ |grep .ssh` ]; then
    mkdir ~/.ssh
    chmod 700 ~/.ssh
fi
END

if [ $? -ne 0 ]; then
    echo "ssh failed"
    exit_on_error
fi
echo "OK"
    
echo "authorizing $HOST_TO_AUTH for automatic SSH use ..."
authorized_keys="~/.ssh/authorized_keys"
ssh $USER@$HOST_TO_AUTH <<END
cat ~/$remote_key >> $authorized_keys
rm ~/$remote_key
chmod 600 $authorized_keys
END

if [ $? -ne 0 ]; then
    echo "ssh failed"
    exit_on_error
fi
echo "OK"

cleanup
echo "Good news $USER: authorization successful!  You can now login automatically to $HOST_TO_AUTH"
exit 0