# GCP Congestion Control Experiment

## Overview

This project aims to compare the performance of two congestion control algorithms, BBR and Cubic, using Google Cloud Platform (GCP) instances. The experiment involves setting up two GCP instances and running a series of tests to analyze the behavior of the BBR and Cubic algorithms under various network conditions.

## Prerequisites

- Google Cloud Platform (GCP) account
- GCP project with billing enabled
- GCP SDK installed locally
- Authentication configured for GCP SDK

## Setup

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/your-username/gcp-congestion-control-experiment.git
    cd gcp-congestion-control-experiment
    ```

2. Run the initialization scripts for both host instances in parallel:

    ```bash
    ./setup/initialize_host1.sh &
    ./setup/initialize_host2.sh &
    wait
    ```

## Running the Experiment

Execute the following command to run the congestion control experiment:

```bash
./run_experiments.sh
```

### Results

The experiment results, including plots and analysis, can be found in the `./figures` folder. Explore these results to understand the comparative performance of BBR and Cubic congestion control algorithms under different scenarios.

### Cleanup

To avoid incurring additional costs, make sure to stop and delete the GCP instances when the experiment is complete:

```bash
gcloud compute instances stop host-1 host-2
gcloud compute instances delete host-1 host-2
