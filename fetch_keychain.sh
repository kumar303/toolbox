#!/bin/bash

# fetches my keychain from home
REMOTE_SERVER=incognito.no-ip.org
KEYCHAIN=$USER.keychain
KEYCHAIN_PATH=~/Library/Keychains
REMOTE_KEYCHAIN_PATH="~"

echo "fetching keychain from $REMOTE_SERVER ..."
scp $USER@$REMOTE_SERVER:$REMOTE_KEYCHAIN_PATH/$KEYCHAIN $KEYCHAIN_PATH/$KEYCHAIN
if [ $? -ne 0 ]; then
    echo "scp failed"
    exit 1
fi
echo "fetched $KEYCHAIN successfully ..."

# can't seem to find a command for "relaunch"
osascript -e "tell Application \"Keychain Access\" to quit"
osascript -e "tell Application \"Keychain Access\" to activate"