# cd3w

## Builds

To run with the local build download the apropriate build zip file from Teams and extract it to the builds directory. You should then be able to run the main.py script.

## Install Slurk (without Docker)
Slurk should be installed on any host machines (machines from which we start an experiment)
The below steps can also be found in https://clp-research.github.io/slurk/slurk_prerequisites.html 2.4 and 2.6 (Steps 1.-2.).
### 1. Generate a ssh key pair (with defaults):
$ ssh-keygen

### 2. Upload or copy the generated public key to your github SSH settings

### 3. Clone the repository.
$ git clone git@github.com:clp-research/slurk.git

### 4. Go into the slurk top directory.

### (Optional) Create and activate a virtual environment.

### 6. Install dependencies:
$ pip install -r requirements.txt

## Running experiments
Note that the implementation of this is still a WIP

### 1. Open a terminal and run the slurk start_server bash script (from the Slurk top directory)
This was imported when installing Slurk (see above). The below step corresponds to https://clp-research.github.io/slurk/slurk_prerequisites.html 2.6 (Step 3.).
$ scripts/start_server.sh

### 2. Copy the admin token at the end of the resulting output
This should look similar to the below (but the token will be a different one, so do not simply copy the below example):

admin token:
01234567-89ab-cdef-0123-456789abcdef

### 3. Open a second terminal and run the main Python script, specifying the parameters for admin token (see step 2.) and optionally the mission level and scene variant (if level and variant aren't specified, the script will run the test configuration).

$ python main.py --token --user --level --variant

e.g.

$ python main.py -token "01234567-89ab-cdef-0123-456789abcdef" --user "1" --level "l0" --version "v0"