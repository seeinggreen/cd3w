


class SlurkSession:


    def __init__(self, ADMIN_TOKEN) -> None:


        """
        reference to this flow: 
            
            1. https://clp-research.github.io/slurk/slurk_gettingstarted.html
            2. 
        """

        # create layout
        # get layout id
        self.layout_id = self.createLayout()


        # create room
        # get room id
        self.room_id =  self.createRoom()

        
        # for each agent
            # create permissions for the agent
            # get agents token
        self.instanciateAgent()




        # get image from ai2thor
        self.getImageFromAI2thor()
        # host image (locally or in google drive)
        # get function
        self.publishImage()


        # initialise log collection
        self.initLogCollection()



    # Private methods
    def createLayout(self):

        pass


    def createRoom(self):
        pass


    def instanciateAgent(self):
        pass


    def getImageFromAI2thor(self):
        pass


    def publishImage(self):
        pass


    def initLogCollection(self):
        pass



    # PUBLIC methods
    def getImageURL(self):
        pass

    def publishAndGetImageURL(self):
        self.getImageFromAI2thor()
        self.publishImage()
        
        return self.getImageURL()

    
    def getLogs(self):
        pass
