from ithor_controller import IthorController;

local_build_path = "../ai2thor/unity/builds/thor-Linux64-local/thor-Linux64-local";
image_dir = "Images/";

if __name__ == "__main__":
    #Set up controller and move the view to the table
    ic = IthorController(height=1200,width=1600,local_exec_path=local_build_path,field_of_view=120,image_dir=image_dir);
    ic.init_scene(pos=[0.25,1,0], rot=270, horizon=70);
    
    for x in range(6):
        for y in range(3):
            if y == 2 and (x == 2 or x == 3): continue;
            ic.place_object('Square3',x,y);
            ic.place_object('Apple1', x, y);
            ic.save_img("{}_{}.png".format(x,y));