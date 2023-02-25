from api_ctrls.api_ctrl import *


def upload_file_img(image_data):

    """
    replace this with an imported function that uploads to:
    - google drive public folder
    - localhost

    based on environmental variables
    """

    return "url"


class SlurkSession:


    def __init__(self, ADMIN_TOKEN) -> None:


        """
        reference to this flow: 
            
            1. https://clp-research.github.io/slurk/slurk_gettingstarted.html
            2. https://clp-research.github.io/slurk/slurk_multibots.html
            3. https://clp-research.github.io/slurk/slurk_layouts.html

        """

        # create layout
        # get layout id
        self.__layout_id = self.__createLayout()


        # create room
        # get room id
        self.__room_id =  self.__createRoom()

        
        # for each agent
            # create permissions for the agent
            # get agents token
        self.__instanciateAgent()


        # get current AI2thor image and publish it
        self.__publishImage()


        # initialise log collection
        self.__initLogCollection()



    # Private methods
    def __createLayout(self):
        pass


    def __createRoom(self):
        pass


    def __instanciateAgent(self):
        pass


    def __getImageFromAI2thor(self):
        pass


    def __publishImage(self):
        # get image from ai2thor
        img = self.__getImageFromAI2thor()
        # host image (locally or in google drive)
        
        self.__img_url = upload_file_img(img)


    def __initLogCollection(self):
        pass



    # PUBLIC methods
    def getImageURL(self):
        return self.__img_url

    def publishAndGetImageURL(self):
        self.__getImageFromAI2thor()
        self.__publishImage()
        
        return self.getImageURL()

    
    def getLogs(self):
        pass
