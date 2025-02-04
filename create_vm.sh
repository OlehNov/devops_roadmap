#!/bin/bash

echo "Enter VM_NAME name: "
read VM_NAME

echo "Enter VM_MEMORY in Mb: "
read VM_MEMORY

echo "Enter VM_CPUS amount: "
read VM_CPUS

echo "Enter HOME path to VM_DISK: "
read HOME

echo "Enter VM_DISK_SIZE in Mb: "
read VM_DISK_SIZE

echo "Enter Path to ISO_IMAGE: "
read ISO_PATH

VM_DISK="${HOME}/${VM_NAME}.vdi"
BRIDGE_ADAPTER=$(ip -br r sh default | awk '{print $5}')

function _error(){
      echo "Error: Something went wrong."
      exit 1
}

if ! VBoxManage createvm --name "${VM_NAME}" --ostype Ubuntu_64 --register; then _error; fi

if ! VBoxManage modifyvm "${VM_NAME}" --memory "${VM_MEMORY}" --cpus "${VM_CPUS}" --nic1 bridged --bridgeadapter1 "${BRIDGE_ADAPTER}"; then _error; fi

if ! VBoxManage createhd --filename "${VM_DISK}" --size "${VM_DISK_SIZE}"; then _error; fi

if ! VBoxManage storagectl "${VM_NAME}" --name "SATA Controller" --add sata --controller IntelAHCI; then _error; fi

if ! VBoxManage storageattach "${VM_NAME}" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "${VM_DISK}"; then _error; fi

if [ ! -e "${ISO_PATH}" ]; then
  echo "Error: ISO file [${ISO_PATH}]"
  exit 1
fi
if ! VBoxManage storageattach "${VM_NAME}" --storagectl "SATA Controller" --port 1 --device 0 --type dvddrive --medium "${ISO_PATH}" || exit 1

echo "Your virtual machine "${VM_NAME}" was created"
