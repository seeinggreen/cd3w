from ai2thor.controller import Controller;
import cv2;
import os;

local_build_path = "/home/dan/Downloads/ai2thor-main/unity/builds/thor-Linux64-local/thor-Linux64-local";
image_dir = "/home/dan/Documents/CA/Images";

if __name__ == "__main__":
    controller = Controller(height=1200,width=1600,local_executable_path=local_build_path,
                            fieldOfView=120,snapToGrid=False,image_dir=image_dir);
    controller.step(action="Teleport",position=dict(x=0.25,y=1,z=0),rotation=dict(x=0,y=270,z=0),horizon=70,forceAction=True)
    event = controller.step(action="Done");
    img = event.cv2img;
    cv2.imwrite(os.path.join(image_dir,"test.png"),img);
    #controller.stop();