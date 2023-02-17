from src.ithor_controller import IthorController;
from src.table import Table;
import platform;
import os;
from src.exceptions import UnsupportedSystemError;
from src.exceptions import MissingBuildFileError;

image_dir = "images/";

def get_local_build_path():
    """
    Checks the system in use and ensures appropriate local build files are present.

    Raises
    ------
    MissingBuildFileError
        Raises MissingBuildFileError if the system is Linux or MacOS but the build files are missing.
    UnsupportedSystemError
        Raises UnsupportedSystemError if the system is Windows or unrecognised.

    Returns
    -------
    string
        The filepath for the appropriate local build files.

    """
    system = platform.system();
    if system == 'Darwin':
        if not os.path.exists("builds/thor-OSXIntel64-local/thor-OSXIntel64-local"):
            raise MissingBuildFileError("You do not have the local build files for MacOS, please download them and put them in the builds directory.");
        else:
            return "thor-OSXIntel64-local";
    elif system == 'Linux':
        if not os.path.exists("builds/thor-Linux64-local/thor-Linux64-local"):
            raise MissingBuildFileError("You do not have the local build files for Linux, please download them and put them in the builds directory.");
        else:
            return "builds/thor-Linux64-local/thor-Linux64-local";
    elif system == 'Windows':
        raise UnsupportedSystemError("Windows is not supported by iTHOR, please use Linux or MacOS.")
    else:
        raise UnsupportedSystemError("The system you are using is unrecognised, please use Linux or MacOS.")

if __name__ == "__main__":
    
    #Get local build path
    local_build_path = get_local_build_path();
    
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
    goal_objects[0][0] = "Vase1";
    goal_objects[0][2] = "Plate1";
    goal_objects[1][0] = "Cup1";
    goal_objects[3][0] = "Bread2Slice";
    
    #Create a Table object with the mats and goal_objects specified
    table = Table(mats,goal_objects);
 
    #Set up controller and move the view to the table
    ic = IthorController(height=1200,width=1600,local_exec_path=local_build_path,field_of_view=120,image_dir=image_dir,table=table);
    ic.init_scene(pos=[0.25,1,0], rot=270, horizon=70);
    
    #Use the information in the Table object to place the assets in the scene
    ic.place_assets();
    
    #Save an image of the goal state and stop the controller
    ic.save_img("goal_state.png");
    ic.stop();