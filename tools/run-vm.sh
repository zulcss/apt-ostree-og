#!/bin/bash

name=$1
if [ -z $name ]; then
  name=apt-ostree
fi

virt-install \
	--connect qemu:///system \
	--boot loader=/usr/share/ovmf/OVMF.fd \
	--machine q35 \
	--name apt-ostree \
	--ram 8096 \
	--vcpus 4 \
	--os-variant debiantesting \
	--disk path=/var/tmp/apt-ostree/build/image/debian-ostree-qemu-uefi-amd64.img \
	--noautoconsole \
	--check path_in_use=off \
	--import
