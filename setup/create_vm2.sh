source ./../settings.sh
source create_vms.sh

make_vm ${NAME2} ${PROJECT} ${ZONE}
upgrade_kernel ${NAME2} ${PROJECT} ${ZONE}
wait_for_reboots ${NAME2} ${PROJECT} ${ZONE}
install_deps ${NAME2} ${PROJECT} ${ZONE}
