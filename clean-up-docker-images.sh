#!/bin/bash
echo "removing all stopped containers"
# This actually tries to remove them all but it will trigger an error if one is
# running.
docker rm $(docker ps -a -q)
echo "removing dangling images"
docker images -q --filter "dangling=true" | xargs docker rmi
