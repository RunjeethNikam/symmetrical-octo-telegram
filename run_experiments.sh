source settings.sh

echo "Running all experiments"
gcloud compute ssh --project $PROJECT --zone $ZONE $NAME1 --command "cd ~/bbr-replication && bash create_figures.sh"
echo "Downloading the figures"
gcloud compute scp --recurse --project $PROJECT --zone $ZONE $NAME1:~/bbr-replication/figures ./
