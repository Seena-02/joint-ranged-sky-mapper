# Sky Mapper

## 1. Clone the Repository

```bash
# Clone Repository
git clone https://github.com/Seena-02/titan-providence
```

## 2. Set Up Environment

We will primarily use [anaconda](https://www.anaconda.com/download) to manage all packages and dependencies. Create a new conda environment and activate it by running the following commands

```bash
# Create Anaconda Env
conda create -n "drone-env" python=3.8.0

# Activate Env
conda activate drone-env
```

## 3. Prerequisites

Install the following dependencies.

```bash
# Install Dependencies
bash get_pi_requirements.sh
```

## 4. Required Software

To execute the simulation, you must install two applications: the first one being [QGroundControl](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/getting_started/download_and_install.html), and the second being [jMAVSim](https://www.youtube.com/watch?v=OtValQdAdrU).
