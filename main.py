from ithor_controller import Ithor_Controller;
import os;

local_build_path = "../ai2thor/unity/builds/thor-Linux64-local/thor-Linux64-local";
image_dir = "Images/";

if __name__ == "__main__":
    #Set up controller and move the view to the table
    ic = Ithor_Controller(height=1200,width=1600,local_exec_path=local_build_path,field_of_view=120,image_dir=image_dir);
    #ic.init_scene(pos=[0.25,1,0], rot=270, horizon=70);


    #ic.place_object('Square1', 0, 0);
    #ic.place_object('Circle1', 1, 0);
    #ic.place_object('Apple1', 2, 0);
    #ic.place_object('Apple3', 3, 0);
    
    #Update display and save start image
    #ic.save_img(os.path.join(image_dir,"start.png"));
    
    #ic.place_object('Apple1', 0, 0);
    #ic.place_object('Apple3', 1, 0);

    #Update display and save end image
    #ic.controller.step(action="Done")
    #ic.save_img(os.path.join(image_dir,"end.png"));
    
    #for x in range(6):
    #    for y in range(3):
    #        ic.place_object('Square3',x,y,True);
    #        ic.place_object('Apple1', x, y,False);
    #        ic.save_img(os.path.join(image_dir,"{}_{}.png".format(x,y)))
            

    import cv2;
    event = ic.controller.step(action="AddThirdPartyCamera", position={'x': 1.2, 'y': 2.03, 'z': -0.026},rotation={'x': 45.93, 'y': -90, 'z': 0},orthographic=False,fieldOfView=60);

    
    for x in range(6):
        for y in range(3):
            ic.place_object('Square3',x,y,True);
            ic.place_object('Apple1', x, y,False);
            im_bgr = cv2.cvtColor(ic.controller.last_event.third_party_camera_frames[0], cv2.COLOR_RGB2BGR);
            cv2.imwrite(os.path.join(image_dir,"{}_{}.png".format(x,y)),im_bgr);
    ic.controller.stop();