# This script/function installs dependencies on a remote VM using gcloud compute ssh.
install_dependencies() {
    # Parameters:
    # $1: VM instance name
    # $2: Google Cloud project name
    # $3: Google Cloud zone

    # Example usage:
    # install_dependencies "instance-1" "my-gcp-project" "us-central1-a"

    # Extract parameters for better readability
    NAME="$1"
    PROJECT="$2"
    ZONE="$3"

    # Inform user about the installation process
    echo "Installing dependencies on $NAME..."

    # SSH into the VM and execute the installation script
    gcloud compute ssh --zone "$3" --project "$2" "$1" --command "cd ~/experiment/setup && bash dependencies.sh"
}


# Function to create a Google Cloud VM instance and copy files to it.
create_host() {
    # Accepts three parameters: HOST_NAME, PROJECT_NAME, and ZONE for VM configuration.

    # Displaying a message indicating the start of VM creation.
    echo "Creating compute engine($1) in GCP  in $2"

    # Creating the VM instance using the 'gcloud compute instances create' command.
	gcloud compute instances create "$1" \
		--project "$2" \
		--zone "$3" \
		--image "https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20231030" \
		--boot-disk-size "30" \
        --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring.write","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly"

    # Storing the exit code of the 'gcloud compute instances create' command.
    host_created=$?

    # Displaying a message indicating the start of file copying.
    echo "Copying experiment logic to the to the host $1"

    # Loop to wait for SSH access to become available.
    until gcloud compute ssh --zone "$3" --project "$2" "$1" --command "mkdir -p experiment"
    do
        # Checking if VM creation was successful (exit code is 0).
        if [ $host_created ];
        then
            echo "Trying to connect to the host $1"
            sleep 2
        else
            # Break the loop if VM creation failed.
            break
        fi
    done;

    # Copying files from the current directory to the VM's 'bbr-replication' directory.
    gcloud compute copy-files --project "$2" --zone "$3" ../* "$1:~/experiment"
}


upgrade_kernel() {
	# Function to upgrade the kernel on a Google Cloud VM instance.
	#
	# This function takes three arguments:
	#   - NAME: The name of the VM instance.
	#   - PROJECT: The Google Cloud project ID where the VM is located.
	#   - ZONE: The zone in which the VM is running.
	#
	# It installs a new kernel on the specified VM instance using SSH and a provided script.
	#
	# Example usage:
	#   upgrade_kernel my-instance my-project us-central1-a
	#
	# Parameters:
	#   $1 - NAME: The name of the VM instance.
	#   $2 - PROJECT: The Google Cloud project ID.
	#   $3 - ZONE: The zone where the VM is located.
	#
	# Dependencies:
	#   - Google Cloud SDK (gcloud) must be installed and authenticated.
	#   - The VM instance must have internet access for kernel updates.
	#
	# Note: Ensure that you have appropriate permissions to execute this operation.

    echo "initializing the kernel on $1"
    gcloud compute ssh --zone "$3" --project "$2"  "$1" --command "cd ~/experiment/setup && bash kernel.sh"
}

# This Function/script waits for a VM to reboot by periodically checking its status.
wait_for_reboots() {
    # Parameters:
    # $1: Name of the VM instance
    # $2: Google Cloud project name
    # $3: Google Cloud zone

    # Example usage:
    # wait_for_reboots "instance-1" "my-gcp-project" "us-central1-a"

    # Check if the VM has rebooted successfully
    until gcloud compute ssh --zone "$3" --project "$2" "$1" --command "echo $1 Rebooted!"
    do  
        # Wait for 2 seconds before checking again
        sleep 2

        # Inform the user about the waiting process
        echo "Waiting for $1 to reboot..."
    done
}

# 
# This Function/script establishes a secure connection between two VMs by sharing SSH keys and IP addresses.
link_vms() {
    # Parameters:
    # $1: Name of the first VM instance
    # $2: Name of the second VM instance
    # $3: Google Cloud project name
    # $4: Google Cloud zone

    # Example usage:
    # link_vms "instance-1" "instance-2" "my-gcp-project" "us-central1-a"


    # Share the IP address of the second VM with the first VM and save it
    gcloud compute ssh --project "$3" --zone "$4" "$2" --command 'hostname -I' | \
    gcloud compute ssh --project "$3" --zone "$4" "$1" --command 'cat > ~/.bbr_pair_ip'

    # Share the SSH public key from the first VM with the second VM
    gcloud compute ssh --project "$3" --zone "$4" "$1" --command 'cat ~/.ssh/id_rsa.pub' | \
    gcloud compute ssh --project "$3" --zone "$4" "$2" --command 'cat >> ~/.ssh/authorized_keys'

}
