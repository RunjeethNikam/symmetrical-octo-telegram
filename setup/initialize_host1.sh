source ./../configurations.sh
source common_utils.sh

create_host ${HOST_1} ${GCLOUD_PROJECT} ${ZONE} 
upgrade_kernel ${HOST_1} ${GCLOUD_PROJECT} ${ZONE}
wait_for_reboots ${HOST_1} ${GCLOUD_PROJECT} ${ZONE}
install_dependencies ${HOST_1} ${GCLOUD_PROJECT} ${ZONE}
