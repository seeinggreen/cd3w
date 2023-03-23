# cd3w

## 1 Builds

To run with the local build download the apropriate build zip file from Teams and extract it to the builds directory (you should end up with ```cd3w/builds/thor-Linux64-local``` or similar). You should then be able to run the main.py script.

## 2 Setting up Slurk

Slurk should be installed on any host machines (machines from which we start an experiment)
The below steps can also be found in https://clp-research.github.io/slurk/slurk_prerequisites.html 2.4 and 2.6 (Steps 1.-2.).

### 2.1 Clone the Slurk Github repository

Add the slurk repo (https://github.com/clp-research/slurk/) to the project folder (resulting in ```/cd3w/slurk```) either by downloading and unziping the repo into the correct folder or running a ```git clone``` command from the ```cd3w``` folder.. 

### 2.2 Install dependencies

Set up a new Python environment with Python 3.9, (e.g. with conda):
```
conda create -n cd3w python=3.9
```
With the new environment activated, install the dependencies using pip from the file in the top level directory (be sure it's not another requirements.txt!):

```sh
pip install -r requirements.txt
```

## 3 Running experiments
To run experiments, you need to start a SLURK sever per experiment and have a user join the room.

### 3.1 Start up the Slurk server 

From the top level directory, run:

```sh
cd slurk
scripts/start_server.sh
```
This will start a server on the default port 5000. To set up multiple servers, run the following to use e.g. port 5001:
```sh
cd slurk
export SLURK_PORT=5001
scripts/start_server.sh
```

### 3.2 Setting up the room
In a separate terminal (with your environment from above active), run the following to set up a room with a huamn user (after starting the SLURK server), with a specified port, level and variant:
```
python src/main.py --port 5000 --level l0 --variant v1
```
The first line of output will be the user token for the human user, e.g.:
```
87cfcc61-37d2-47cf-b336-50897dd6b30e
```

### 3.3 Linking to the room
To let users enter the room, they should go to ```192.168.xxx.xxx:500x``` (you will need to check the IP address of your local machine and tell the users which port their room is using). They may enter any name but need to enter the token from above. The room will give instructions automatically.
