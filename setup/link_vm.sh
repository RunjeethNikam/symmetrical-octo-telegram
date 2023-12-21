# Import configuration files
source ./../custom_config.sh
source utilities.sh    # COMMON_UTILITIES.SH 

# Connect VMs with specified parameters
establish_connection "$CUSTOM_HOST_1" "$CUSTOM_HOST_2" "$CUSTOM_PROJECT" "$CUSTOM_ZONE"
