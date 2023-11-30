source ./../settings.sh
source create_vms.sh

make_vm ${NAME1} ${PROJECT} ${ZONE}
upgrade_kernel ${NAME1} ${PROJECT} ${ZONE}
wait_for_reboots ${NAME1} ${PROJECT} ${ZONE}
install_deps ${NAME1} ${PROJECT} ${ZONE}
