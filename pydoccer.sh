#!/bin/bash

PYDOC=`which pydoc`
if [ ! -x ${PYDOC} ]
then
    echo "could not find executable pydoc (tried: ${PYDOC})"
    exit 1
fi

PYDOC_PORT=9000
PYDOC_SERVER=http://localhost:${PYDOC_PORT}/
running=0
pydoc_pses=0

function browse_docs()
{
    open ${PYDOC_SERVER}
}

for ps in `ps ax | grep "${PYDOC}" | awk '{ print $1 }'`
do
    let pydoc_pses++
done

if [ $pydoc_pses -ge 2 ]
then
    browse_docs
else
    ${PYDOC} -p ${PYDOC_PORT} &
    until `curl -o /dev/null ${PYDOC_SERVER} &>/dev/null`
    do
        echo "waiting for pydoc server ..."
        sleep 2
    done
    browse_docs
fi
exit 0