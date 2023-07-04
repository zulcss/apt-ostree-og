#!/bin/bash
#
mkdir -p output
docker run --rm -i -t \
	--device /dev/kvm \
	--privileged \
	-v $(pwd):/usr/src/apt-ostree \
	-v $(pwd)/output:/var/tmp \
	-v /var/run/docker.sock:/var/run/docker.sock \
	apt-ostree
       
