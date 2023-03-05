# cd3w

## 1 Builds

To run with the local build download the apropriate build zip file from Teams and extract it to the builds directory. You should then be able to run the main.py script.

## 2 Setting up Ithor

TBC

## 3 Setting up Slurk (without Docker)

Slurk should be installed on any host machines (machines from which we start an experiment)
The below steps can also be found in https://clp-research.github.io/slurk/slurk_prerequisites.html 2.4 and 2.6 (Steps 1.-2.).

### 3.1 Generate a ssh key pair

```sh
ssh-keygen
```

Copy the generated public key to your github SSH settings

### 3.2 Clone the Slurk Github repository

```sh
git clone git@github.com:clp-research/slurk.git
```

### 3.3 Install dependencies

```sh
sudo apt-get install jq curl
pip install -r requirements.txt
```

## 4 Running experiments

# 4.0 Start up the Slurk server 

From the top level directory, run:

```sh
cd slurk
scripts/start_server.sh
```

**Note:** You may need to kill any Slurk processes running in the background by running the below command to get the id(s) of the running process(es)

```sh
lsof -i :5000 | grep LISTEN
```

and then running the following to kill any processes still running:

```sh
kill -9 {PROCESS_ID} 
```

### 4.1 Running without Concierge Bot

#### 4.1.1 Create a room and task

In a second terminal, from the top level directory, run:

```sh
TASK_LAYOUT_ID=$(slurk/scripts/create_layout.sh src/slurk/layouts/task_room_layout.json | jq .id)
TASK_ROOM_ID=$(slurk/scripts/create_room.sh $TASK_LAYOUT_ID | jq .id)
echo "TASK_ROOM_ID=$TASK_ROOM_ID"
```

#### 4.1.1 Run IthorBot

In a third terminal, from the top level directory, copy over `TASK_ROOM_ID=<value-from-second-terminal>` and run:

```sh
ITHOR_TOKEN=$(slurk/scripts/create_room_token.sh $TASK_ROOM_ID src/slurk/permissions/ithor_bot_permissions.json | jq -r .id)
ITHOR_USER=$(slurk/scripts/create_user.sh "IthorBot" $ITHOR_TOKEN | jq .id)
python src/main.py --token $ITHOR_TOKEN --user $ITHOR_USER --level <level> --variant <variant>
```

#### 4.1.4 Create user tokens for the room

Back in the second terminal, let’s create two user tokens (run the command twice):

```sh
slurk/scripts/create_room_token.sh $TASK_ROOM_ID src/slurk/permissions/user_permissions.json 1 | jq .id
```

Share the output with a particpicant to be used to log into the slurk room.

### 4.2 Running with Concierge Bot
#### 4.2.1 Create a waiting room

**Note:** you may need to run `sudo apt  install jq curl` before the next steps...

In a second terminal, from the top level directory, run:

```sh
WAITING_ROOM_LAYOUT_ID=$(slurk/scripts/create_layout.sh src/slurk/layouts/waiting_room_layout.json | jq .id)
WAITING_ROOM_ID=$(slurk/scripts/create_room.sh $WAITING_ROOM_LAYOUT_ID | jq .id)
echo "WAITING_ROOM_LAYOUT_ID=$WAITING_ROOM_LAYOUT_ID"
```

#### 4.2.2 Create a task

In the same terminal, from the top level directory, run:

```sh
TASK_LAYOUT_ID=$(slurk/scripts/create_layout.sh slurk/examples/simple_layout.json | jq .id)
TASK_ID=$(slurk/scripts/create_task.sh  "Data Collection Task" 2 $TASK_LAYOUT_ID | jq .id)
echo "TASK_ID=$TASK_ID"
```

**Note:** this sets up a task called "Data Collection Task" which is meant for 2 participants

#### 4.2.3 Run ConciergeBot

In a third terminal, from the top level directory, run:

```sh
WAITING_ROOM_ID=<value-from-other-terminal>
CONCIERGE_TOKEN=$(slurk/scripts/create_room_token.sh $WAITING_ROOM_ID src/slurk/bots/conciergebot/concierge_bot_permissions.json | jq -r .id)
CONCIERGE_USER=$(slurk/scripts/create_user.sh "ConciergeBot" $CONCIERGE_TOKEN | jq .id)
SLURK_TOKEN=$CONCIERGE_TOKEN SLURK_USER=$CONCIERGE_USER SLURK_PORT=5000 python src/slurk/bots/conciergebot/concierge_bot.py
```

**Note:** you may have to run `chmod +x src/slurk/bots/conciergebot/concierge_bot.py`


#### 4.2.4 Run IthorBot

In a fourth terminal, from the top level directory, run:

```sh
WAITING_ROOM_ID=<value-from-other-terminal>
TASK_ID=<value-from-other-terminal>
ITHOR_TOKEN=$(slurk/scripts/create_room_token.sh $WAITING_ROOM_ID src/slurk/permissions/ithor_bot_permissions.json | jq -r .id)
ITHOR_USER=$(slurk/scripts/create_user.sh "IthorBot" $ITHOR_TOKEN | jq .id)
python src/main.py --token $ITHOR_TOKEN --user $ITHOR_USER --task $TASK_ID --level <level> --variant <variant>
```

#### 4.2.5 Create user tokens for the task

Back in the second terminal, let’s create two user tokens (run the command twice):

```sh
slurk/scripts/create_room_token.sh $TASK_ROOM_ID src/slurk/permissions/user_permissions.json 1 | jq .id
```

Share the output with a particpicant to be used to log into the slurk room.

### 5.2 Ngrok access

Sign up for an ngrok account: https://ngrok.com/. Then run the following in a separate terminal:

```sh
snap install ngrok
ngrok config add-authtoken <your-access-token>
ngrok http 5000
```

Then share the link with participants.