#!/bin/bash

if [ ?{#} -lt 3 ]; then 
    echo "Error: Missing required arguments."
    echo "Usage: ./script.sh <VM_NAME> <ISO_PATH> <HOME_PATH> [<VM_MEMORY> <VM_CPUS> <VM_DISK_SIZE>]"
    exit 1
fi

function _error(){
      echo "Error: ${1}"
      exit 1
}

VM_NAME="$1"
ISO_PATH="$2"
HOME_PATH="$3"
VM_MEMORY="$4"
VM_CPUS="$5"
VM_DISK_SIZE="$6"
OSTYPE="Ubuntu_64"

if [ -z "$VM_MEMORY" ]; then VM_MEMORY=1024; fi
if [ -z "$VM_CPUS" ]; then VM_CPUS=1; fi
if [ -z "$VM_DISK_SIZE" ]; then VM_DISK_SIZE=6000; fi

VM_DISK="${HOME_PATH}/${VM_NAME}.vdi"

BRIDGE_ADAPTER=$(ip -br r sh default | awk '{print $5}')

if ! VBoxManage createvm --name "${VM_NAME}" --ostype '${OSTYPE}' --register; then _error "Failed to create VM"; fi

if ! VBoxManage modifyvm "${VM_NAME}" --memory "${VM_MEMORY}" --cpus "${VM_CPUS}" --nic1 bridged --bridgeadapter1 "${BRIDGE_ADAPTER}"; then _error "Failed to modify VM"; fi

if ! VBoxManage createhd --filename "${VM_DISK}" --size "${VM_DISK_SIZE}"; then _error "Failed to create virtual disk"; fi

if ! VBoxManage storagectl "${VM_NAME}" --name "SATA Controller" --add sata --controller IntelAHCI; then _error "Failed to add storage controller"; fi

if ! VBoxManage storageattach "${VM_NAME}" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "${VM_DISK}"; then _error "Failed to attach HDD"; fi

if ! VBoxManage storageattach "${VM_NAME}" --storagectl "SATA Controller" --port 1 --device 0 --type dvddrive --medium "${ISO_PATH}"; then _error "Failed to attach ISO"; fi

echo "Your virtual machine '${VM_NAME}' was created"
