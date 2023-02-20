import json

from requests import post, get, patch, put, delete



# ENVIRONMENTAL VARIABLES
baseUrl = "http://0.0.0.0:5000"
admin_token = "Bearer 00000000-0000-0000-0000-000000000000"



# HTTP helper functions

def get_main_headers(admin_token):
    return {
        "Authorization" : admin_token,
        "Content-Type": "application/json"
    }



def exec_req(req_fun, urlPath="", qparams=None, data_dict=None, hdrs=None):

    headers = get_main_headers(admin_token)
    
    if hdrs:
        header_dict = hdrs | headers
    else:
        header_dict = headers
    
    try:
        url = baseUrl + "/slurk/api/" + urlPath
        
        response = req_fun(
            url,
            json=json.dumps(data_dict),
            headers=hdrs,
            params=qparams
        )
        
        
        return response.json()
            
    except:
        print("ERROR")
        return None
    
    return None
    

    
# HTTP request functions

def _get(urlPath="", qparams=None, hdrs=None):
    return exec_req(get, urlPath, qparams, hdrs=hdrs)

def _delete(urlPath="", qparams=None, hdrs=None):
    return exec_req(delete, urlPath, qparams, hdrs=hdrs)

def _post(urlPath="", qparams=None, data_dict=None, hdrs=None):
    return exec_req(post, urlPath, qparams, data_dict=data_dict, hdrs=hdrs)

def _patch(urlPath="", qparams=None, data_dict=None, hdrs=None):
    return exec_req(patch, urlPath, qparams, data_dict=data_dict, hdrs=hdrs)


    
# API generic operation functions

joinPaths = lambda l,r: l + "/" + r
getInstancePath = lambda path, instance_id: joinPaths(
    path, 
    str(instance_id)
)

def getMultipleInstances(routeName, qparams=None, hdrs=None):
    return _get(
        routeName, 
        qparams=None, 
        hdrs=None
    )

def createInstance(routeName, data_dict=None, qparams=None, hdrs=None):
    return _post(
        routeName, 
        data_dict=None,
        qparams=None,
        hdrs=None
    )

def getInstance(routeName, instance_id, hdrs=None):
    return _get(
        getInstancePath(routeName, instance_id), 
        qparams=None, 
        hdrs=None
    )

def updateInstance(routeName, instance_id, data_dict=None, hdrs=None):
    return _patch(
        getInstancePath(routeName, instance_id), 
        data_dict=None, 
        qparams=None, 
        hdrs=None
    )

def deleteInstance(routeName, instance_id, hdrs=None):
    return _delete(
        getInstancePath(routeName, instance_id), 
        qparams=None, 
        hdrs=None
    )
    

    

# INIT ENTITIES DATA HELPER FUNCTIONS

def init_default_layout_data(title, subtitle, merging_dict={}):
    return {
        "title": title,
        "subtitle": subtitle,
        "scripts": {
            "incoming-text": "display-text",
            "incoming-image": "display-image",
            "submit-message": "send-message",
            "print-history": "plain-history"
        }
    } | merging_dict


def init_default_openvidu_session_data(merging_dict={}):
    return {
    } | merging_dict


def init_default_room_data(layout_id, openvidu_session_id, merging_dict={}):
    return {
      "layout_id": layout_id,
      "read_only": False,
      "openvidu_session_id": openvidu_session_id
    } | merging_dict


def init_default_permission_data(merging_dict={}):
    return {
      "api": True
    } | merging_dict


def init_default_token_data(permissions_id, room_id, task_id, merging_dict={}):
    return {
      "permissions_id": permissions_id,
      "registrations_left": 1,
      "room_id": room_id,
      "task_id": task_id,
      "openvidu_settings": {
        "start_with_audio": True,
        "start_with_video": True,
        "video_resolution": "",
        "video_framerate": 26858808,
        "video_min_recv_bandwidth": 55874486,
        "video_max_recv_bandwidth": -53424848,
        "video_min_send_bandwidth": 44957958,
        "video_max_send_bandwidth": 59637031,
        "video_publisher_location": "ipsum eu",
        "video_subscribers_location": "labore aute eu reprehenderit",
        "allowed_filters": [
          "repreh",
          "consequat"
        ]
      }
    } | merging_dict


def init_default_user_data(name, token_id, merging_dict={}):
    return {
      "name": "ipsum ",
      "token_id": "8f969f52-64a9-db95-cadf-8598f5b24da4"
    } | merging_dict


def init_default_task_data(name, layout_id, num_users=2, merging_dict={}):
    return {
      "layout_id": layout_id,
      "name": name,
      "num_users": num_users
    } | merging_dict


def init_default_log_data(event_name, user_id, room_id, receiver_id, num_users=2, merging_dict={}):
    return {
      "event": event_name,
      "user_id": user_id,
      "room_id": room_id,
      "receiver_id": receiver_id,
      "data": {}
    } | merging_dict

# ENTITIES API calls


# LAYOUTS
def getMultipleLayouts(qparams=None, hdrs=None):
    return getMultipleInstances("layouts", qparams=qparams, hdrs=hdrs)

def createLayout(title, subtitle, data_dict=None, qparams=None, hdrs=None):
    init_data = init_default_layout_data(title, subtitle)
    return createInstance("layouts", data_dict=init_data, qparams=qparams, hdrs=hdrs)

def getLayout(instance_id, hdrs=None):
    return getInstance("layouts", instance_id, hdrs=hdrs)

def updateLayout(instance_id, data_dict=None, hdrs=None):
    return updateInstance("layouts", instance_id, data_dict=data_dict, hdrs=hdrs)

def deleteLayout(instance_id, hdrs=None):
    return deleteInstance("layouts", instance_id, hdrs=hdrs)


# OPENVIDU SESSIONS
def getMultipleOpenviduSessions(qparams=None, hdrs=None):
    return getMultipleInstances("openvidu/sessions", qparams=qparams, hdrs=hdrs)

def createOpenviduSession(data_dict=None, qparams=None, hdrs=None):
    init_data = init_default_openvidu_session_data()
    return createInstance("openvidu/sessions", data_dict=init_data, qparams=qparams, hdrs=hdrs)

def getOpenviduSession(instance_id, hdrs=None):
    return getInstance("openvidu/sessions", instance_id, hdrs=hdrs)

def updateOpenviduSession(instance_id, data_dict=None, hdrs=None):
    return updateInstance("openvidu/sessions", instance_id, data_dict=data_dict, hdrs=hdrs)

def deleteOpenviduSession(instance_id, hdrs=None):
    return deleteInstance("openvidu/sessions", instance_id, hdrs=hdrs)


# ROOMS
def getMultipleRooms(qparams=None, hdrs=None):
    return getMultipleInstances("rooms", qparams=qparams, hdrs=hdrs)

def createRoom(layout_id, openvidu_session_id, data_dict=None, qparams=None, hdrs=None):
    init_data = init_default_room_data(layout_id, openvidu_session_id)
    return createInstance("rooms", data_dict=init_data, qparams=qparams, hdrs=hdrs)

def getRoom(instance_id, hdrs=None):
    return getInstance("rooms", instance_id, hdrs=hdrs)

def updateRoom(instance_id, data_dict=None, hdrs=None):
    return updateInstance("rooms", instance_id, data_dict=data_dict, hdrs=hdrs)

def deleteRoom(instance_id, hdrs=None):
    return deleteInstance("rooms", instance_id, hdrs=hdrs)


# PERMISSIONS
def getMultiplePermissions(qparams=None, hdrs=None):
    return getMultipleInstances("permissions", qparams=qparams, hdrs=hdrs)

def createPermission(data_dict=None, qparams=None, hdrs=None):
    init_data = init_default_permission_data()
    return createInstance("permissions", data_dict=init_data, qparams=qparams, hdrs=hdrs)

def getPermission(instance_id, hdrs=None):
    return getInstance("permissions", instance_id, hdrs=hdrs)

def updatePermission(instance_id, data_dict=None, hdrs=None):
    return updateInstance("permissions", instance_id, data_dict=data_dict, hdrs=hdrs)

def deletePermission(instance_id, hdrs=None):
    return deleteInstance("permissions", instance_id, hdrs=hdrs)


# TOKENS
def getMultipleTokens(qparams=None, hdrs=None):
    return getMultipleInstances("tokens", qparams=qparams, hdrs=hdrs)

def createToken(permissions_id, room_id, task_id, data_dict=None, qparams=None, hdrs=None):
    init_data = init_default_token_data(permissions_id, room_id, task_id)
    return createInstance("tokens", data_dict=init_data, qparams=qparams, hdrs=hdrs)

def getToken(instance_id, hdrs=None):
    return getInstance("tokens", instance_id, hdrs=hdrs)

def updateToken(instance_id, data_dict=None, hdrs=None):
    return updateInstance("tokens", instance_id, data_dict=data_dict, hdrs=hdrs)

def deleteToken(instance_id, hdrs=None):
    return deleteInstance("tokens", instance_id, hdrs=hdrs)


# USERS
def getMultipleUsers(qparams=None, hdrs=None):
    return getMultipleInstances("users", qparams=qparams, hdrs=hdrs)

def createUser(name, token_id, data_dict=None, qparams=None, hdrs=None):
    init_data = init_default_user_data(name, token_id)
    return createInstance("users", data_dict=init_data, qparams=qparams, hdrs=hdrs)

def getUser(instance_id, hdrs=None):
    return getInstance("users", instance_id, hdrs=hdrs)

def updateUser(instance_id, data_dict=None, hdrs=None):
    return updateInstance("users", instance_id, data_dict=data_dict, hdrs=hdrs)

def deleteUser(instance_id, hdrs=None):
    return deleteInstance("users", instance_id, hdrs=hdrs)


# TASKS
def getMultipleTasks(qparams=None, hdrs=None):
    return getMultipleInstances("tasks", qparams=qparams, hdrs=hdrs)

def createTask(name, layout_id, num_users=2, data_dict=None, qparams=None, hdrs=None):
    init_data = init_default_task_data(name, layout_id, num_users=num_users)
    return createInstance("tasks", data_dict=init_data, qparams=qparams, hdrs=hdrs)

def getTask(instance_id, hdrs=None):
    return getInstance("tasks", instance_id, hdrs=hdrs)

def updateTask(instance_id, data_dict=None, hdrs=None):
    return updateInstance("tasks", instance_id, data_dict=data_dict, hdrs=hdrs)

def deleteTask(instance_id, hdrs=None):
    return deleteInstance("tasks", instance_id, hdrs=hdrs)


# LOGS
def getMultipleLogs(qparams=None, hdrs=None):
    return getMultipleInstances("logs", qparams=qparams, hdrs=hdrs)

def createLog(event_name, user_id, room_id, receiver_id, num_users=2, data_dict=None, qparams=None, hdrs=None):
    init_data = init_default_log_data(event_name, user_id, room_id, receiver_id, num_users=num_users)
    return createInstance("logs", data_dict=init_data, qparams=qparams, hdrs=hdrs)

def getLog(instance_id, hdrs=None):
    return getInstance("logs", instance_id, hdrs=hdrs)

def updateLog(instance_id, data_dict=None, hdrs=None):
    return updateInstance("logs", instance_id, data_dict=data_dict, hdrs=hdrs)

def deleteLog(instance_id, hdrs=None):
    return deleteInstance("logs", instance_id, hdrs=hdrs)

