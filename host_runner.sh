#!/usr/bin/env bash
#-v /home/database/firstland/4th_semester/elec_agent/project/RA_project/RA:/RA_ws/RA \
xhost +local:`docker inspect --format='{{ .Config.Hostname }}' towgroup/ra`
set -x

echo "Searching for Docker image ..."
DOCKER_IMAGE_ID=$(docker images --format="{{.ID}}" towgroup/ra | head -n 1)
echo "Found and using ${DOCKER_IMAGE_ID}"

USER_UID=$(id -u)
docker run -t -i \
  --net host \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=unix$DISPLAY \
  -v /home/database/firstland/4th_semester/elec_agent/project/RA_project/RA_project:/RA_ws/RA \
  ${DOCKER_IMAGE_ID} \
  ${@}


