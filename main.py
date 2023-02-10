from ai2thor.controller import Controller;
import cv2;
import os;

local_build_path = "../ai2thor/unity/builds/thor-Linux64-local/thor-Linux64-local";
image_dir = "/Images/";

if __name__ == "__main__":
    controller = Controller(height=1200,width=1600,local_executable_path=local_build_path,
                            fieldOfView=120,snapToGrid=False,image_dir=image_dir);
    controller.step(action="Teleport",position=dict(x=0.25,y=1,z=0),rotation=dict(x=0,y=270,z=0),horizon=70,forceAction=True)

    controller.step(action="PlaceObjectAtPoint",objectId="Undefined|-00.47|+01.14|+05.42",position={'x': -0.3, 'y': 1.3, 'z': 0.2},rotation={'x':0,'y':0,'z':0})
    controller.step(action="PlaceObjectAtPoint",objectId="Undefined|-00.47|+01.14|+05.42",position={'x': -0.3, 'y': 1.3, 'z': 0.2},rotation={'x':0,'y':0,'z':0})

    controller.step(action="PlaceObjectAtPoint",objectId="Undefined|-00.47|+01.14|+05.91",position={'x': 0, 'y': 1.3, 'z': 0.5},rotation={'x':0,'y':0,'z':0})
    controller.step(action="PlaceObjectAtPoint",objectId="Undefined|-00.47|+01.14|+05.91",position={'x': 0, 'y': 1.3, 'z': 0.5},rotation={'x':0,'y':0,'z':0})
    
    controller.step(action="PlaceObjectAtPoint",objectId="Apple|-00.47|+01.14|+04.99",position={'x': 0.1, 'y': 1.3, 'z': -0.3},rotation={'x':0,'y':0,'z':0})
    controller.step(action="PlaceObjectAtPoint",objectId="Apple|-00.47|+01.14|+04.99",position={'x': 0.1, 'y': 1.3, 'z': -0.3},rotation={'x':0,'y':0,'z':0})
    
    controller.step(action="PlaceObjectAtPoint",objectId="Apple|-00.47|+01.14|+04.52",position={'x': 0.3, 'y': 1.3, 'z': 0.6},rotation={'x':0,'y':0,'z':0})
    controller.step(action="PlaceObjectAtPoint",objectId="Apple|-00.47|+01.14|+04.52",position={'x': 0.3, 'y': 1.3, 'z': 0.6},rotation={'x':0,'y':0,'z':0})

    event = controller.step(action="Done");
    cv2.imwrite(os.path.join(image_dir,"start.png"),event.cv2img);
    
    
    controller.step(action="PlaceObjectAtPoint",objectId="Apple|-00.47|+01.14|+04.99",position={'x': -0.3, 'y': 1.3, 'z': 0.2},rotation={'x':0,'y':0,'z':0})
    controller.step(action="PlaceObjectAtPoint",objectId="Apple|-00.47|+01.14|+04.99",position={'x': -0.3, 'y': 1.3, 'z': 0.2},rotation={'x':0,'y':0,'z':0})
    
    controller.step(action="PlaceObjectAtPoint",objectId="Apple|-00.47|+01.14|+04.52",position={'x': 0, 'y': 1.3, 'z': 0.5},rotation={'x':0,'y':0,'z':0})
    controller.step(action="PlaceObjectAtPoint",objectId="Apple|-00.47|+01.14|+04.52",position={'x': 0, 'y': 1.3, 'z': 0.5},rotation={'x':0,'y':0,'z':0})
    event = controller.step(action="Done")
    
    cv2.imwrite(os.path.join(image_dir,"end.png"),event.cv2img);