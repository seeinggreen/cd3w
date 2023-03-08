# cd3w

## 1 Builds

To run with the local build download the apropriate build zip file from Teams and extract it to the builds directory. You should then be able to run the main.py script.

## 2 Setting up Slurk

Slurk should be installed on any host machines (machines from which we start an experiment)
The below steps can also be found in https://clp-research.github.io/slurk/slurk_prerequisites.html 2.4 and 2.6 (Steps 1.-2.).

### 2.1 Clone the Slurk Github repository

Add the slurk repo (https://github.com/clp-research/slurk/) to the project folder (resulting in ```/cd3w/slurk```) either by downloading and unziping the repo into the correct folder or running a ```git clone``` command from the ```cd3w``` folder.

### 2.2 Install dependencies

Set up a new Python environment with Python 3.9, e.g. (with conda):
```
conda create -n slurk python=3.9
```
With the new environment activated, install the dependencies using pip from the file in the top level directory:

```sh
pip install -r requirements.txt
```

## 3 Running experiments
To run experiments, you need to start a SLURK sever per experiment and have two users join the room.

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
Run the following to set up a room with two users (after starting the SLURK server), with a specified port, level and variant:
```
python src/tokens.py --port 5000 --level l0 --variant v1
```
The first two lines of output will be the user tokens for the two human users, e.g.:
```
User1:87cfcc61-37d2-47cf-b336-50897dd6b30e
User2:0a2be629-95e3-471f-863b-54de088d8c8c
```

### 3.3 Linking to the room
To let users enter the room, they should go to ```192.168.xxx.xxx:500x``` (you will need to check the IP address of your local machine and tell the users which port their room is using). One user should use the name 'follower' and one should use the name 'leader' with each using one of the two user tokens (it doesn't matter which). The room will give instructions automatically.