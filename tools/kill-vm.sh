#!/bin/bash
#
name=$1
if [ -z $name ]; then
   name="apt-ostree"
fi
sudo virsh destroy $name && sudo virsh undefine $name
