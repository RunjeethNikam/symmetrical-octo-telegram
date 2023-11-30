make_vm() {
    NAME=$1
    PROJECT=$2
    ZONE=$3

    echo "Creating VM $NAME in $PROJECT"
    gcloud compute instances create "$NAME" \
	--project "$PROJECT" \
	--zone "$ZONE" \
	--machine-type "n1-standard-4" \
	--network "default" \
	--maintenance-policy "MIGRATE" \
	--boot-disk-type "pd-standard" \
	--boot-disk-device-name "$NAME" \
	--image "https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20231030" \
	--boot-disk-size "30" \
	--scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring.write","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly"
    made_vm=$?

    echo "Copying files to $NAME"
    until gcloud compute ssh --project "$PROJECT" --zone "$ZONE" "$NAME" --command "mkdir -p bbr-replication"
    do
	if [ $made_vm ];
	then
	    echo "Waiting for ssh key to propagate to $NAME..."
	    sleep 2
	else
	    break
	fi
    done;
    gcloud compute copy-files --project "$PROJECT" --zone "$ZONE" ../* "$NAME:~/bbr-replication"
}


upgrade_kernel() {
    NAME=$1
    PROJECT=$2
    ZONE=$3

    echo "Installing kernel on $NAME"
    gcloud compute ssh --project "$PROJECT" --zone "$ZONE" "$NAME" --command "cd ~/bbr-replication/setup && bash install_kernel.sh"
}

install_deps() {
    NAME=$1
    PROJECT=$2
    ZONE=$3

    echo "Installing dependencies on $NAME"
    gcloud compute ssh --project "$PROJECT" --zone "$ZONE" "$NAME" --command "cd ~/bbr-replication/setup && bash install_deps.sh"
}

link_vms() {
    NAME1=$1
    NAME2=$2
    PROJECT=$3
    ZONE=$4

    gcloud compute ssh --project "$PROJECT" --zone "$ZONE" "$NAME1" --command 'cat ~/.ssh/id_rsa.pub' |	gcloud compute ssh --project "$PROJECT" --zone "$ZONE" "$NAME2" --command 'cat >> ~/.ssh/authorized_keys'

    gcloud compute ssh --project "$PROJECT" --zone "$ZONE" "$NAME2" --command 'hostname -I' | gcloud compute ssh --project "$PROJECT" --zone "$ZONE" "$NAME1" --command 'cat > ~/.bbr_pair_ip'
}

wait_for_reboots() {
    NAME=$1
    PROJECT=$2
    ZONE=$3

    until gcloud compute ssh --project "$PROJECT" --zone "$ZONE" "$NAME" --command "echo $NAME Rebooted!"
    do
        echo "Waiting for $NAME to reboot..."
        sleep 2
    done;
}
