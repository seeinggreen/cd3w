from ithor_controller import IthorController;
from table import Table;

local_build_path = "builds/thor-Linux64-local/thor-Linux64-local";
image_dir = "images/";

if __name__ == "__main__":
    
    #Get an empty list of positions and specify which mats go where
    mats = Table.get_empty_slots_list();
    mats[0][0] = "Circle1";
    mats[0][2] = "Circle11";
    mats[1][0] = "Square12";
    mats[1][1] = "Circle13";
    mats[1][2] = "Circle7";
    mats[3][0] = "Square3";
    mats[4][0] = "Square5";
    mats[5][2] = "Circle4";
    
    #Get an empty list and specify goal object positions
    goal_objects = Table.get_empty_slots_list();
    goal_objects[0][0] = "Apple1";
    goal_objects[0][2] = "Apple3";
    goal_objects[1][0] = "Cup1";
    goal_objects[3][0] = "Bowl2";
    
    #Create a Table object with the mats and goal_objects specified
    table = Table(mats,goal_objects);
 
    #Set up controller and move the view to the table
    ic = IthorController(height=1200,width=1600,local_exec_path=local_build_path,field_of_view=120,image_dir=image_dir,table=table);
    ic.init_scene(pos=[0.25,1,0], rot=270, horizon=70);
    
    #Use the information in the Table object to place the assets in the scene
    ic.place_assets();
    
    #Save an image of the goal state and stop the controller
    ic.save_img("goal_state.png");
    ic.controller.stop();