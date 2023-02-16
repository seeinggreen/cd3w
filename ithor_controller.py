#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 10:47:11 2023

@author: dan
"""

from ai2thor.controller import Controller;
from exceptions import DuplicateAssetError;
from exceptions import MissingAssetError;
from items import Items;
import cv2;
import os;

class IthorController:
    
    def __init__(self,height,width,local_exec_path,field_of_view,image_dir,table):
        """
        Constructor to set up the iTHOR controller.

        Parameters
        ----------
        height : int
            The height of the Unity window.
        width : int
            The width of the Unity window.
        local_exec_path : string
            The filepath for the local Unity build.
        field_of_view : int
            The agents field of view.
        image_dir : string
            The filepath for the directory to store output images.

        Returns
        -------
        An Ithor_Controller wrapper object.

        """
        #Set up a standard iTHOR controller
        self.controller = Controller(height=height,
                                width=width,
                                local_executable_path=local_exec_path,
                                fieldOfView=field_of_view,
                                snapToGrid=False);
        self.table = table; #Create a Table object to handle the object grid
        self.image_dir = image_dir;
    
    def init_scene(self,pos,rot,horizon):
        """
        Initalise the scene to place the agent correctly.
        TODO - also set up the objects

        Parameters
        ----------
        pos : list of float
            The three coordinates of the agent position.
        rot : int
            The angle the agent is facing.
        horizon : int
            The vertical angle of the view in 30deg increments.

        Returns
        -------
        None.

        """
        #Physically move the agent to the specified position
        self.controller.step(action="Teleport",
                             position=dict(x=pos[0],y=pos[1],z=pos[2]),
                             rotation=dict(x=0,y=rot,z=0),
                             horizon=horizon,
                             forceAction=True);
        
    def name_to_object_id(self,name):
        """
        Converts an asset name to an iTHOR objectId string.

        Parameters
        ----------
        name : string
            The asset name as specified in the Unity master scene.
            
        Raises
        ------
        DuplicateAssetError
            Will raise a DuplicateAssetError if an asset name appears more than once.
            
        MissingAssetError
            Will raise a MissingAssetError if the asset name cannot be found.

        Returns
        -------
        string
            The objectId given by iTHOR for the asset.

        """
        #Take the metadata from the last event to ensure it's up to date
        objs = self.controller.last_event.metadata['objects'];
        #Get all the objects with that asset name
        named_objs = [o for o in objs if o['name'] == name];
        #Should be a singleton list, so return the objectId of the first entry
        if len(named_objs) > 1:
            raise DuplicateAssetError("{} objects were found for {}, expected just one.".format(len(named_objs),name));
        if len(named_objs) == 0:
            raise MissingAssetError("Could not find the asset called {}.",format(name));
        return named_objs[0]['objectId'];
        
    def pickup(self,name):
        """
        Wrapper function to pickup a named object.

        Parameters
        ----------
        name : string
            The name of the object to pickup.

        Returns
        -------
        None.

        """
        object_id = self.name_to_object_id(name, self.controller.last_event);
        #Objects should be in front of the agent before calling this method
        self.controller.step(action="PickupObject",objectId=object_id);

    def place_assets(self):
        """
        Places all assets specified in the table grid in their locations.

        Returns
        -------
        None.

        """
        grid = self.table.grid;
        for x,column in enumerate(grid):
            for y,slot in enumerate(column):
                if slot.has_mat():
                    self.place_asset(slot.mat,x,y);
                if slot.has_object():
                    self.place_asset(slot.object,x,y);
        
    def place_asset(self,name,x,y):
        """
        Wrapper function to place objects on the table grid.

        Parameters
        ----------
        name : string
            The name of the object to move.
        x : int
            The horizontal grid coordinate to move the object to.
        y : int
            The vertical grid coordinate to move the object to.

        Raises
        ------
        GridCoordinateError
            Will raise a GridCoordinateError if specified coordinates is out of bounds.

        Returns
        -------
        None.

        """
        #Convert the grid coordinates to iTHOR coordinates (can raise GridCoordinateError)
        pos = self.table.grid_to_coords(x,y);
        #Get the objectId using the asset name
        object_id = self.name_to_object_id(name);
        #Place the object with no rotation
        self.controller.step(action="PlaceObjectAtPoint",
                             objectId=object_id,
                             position=pos,
                             rotation={'x':0,'y':0,'z':0});
        
    def save_img(self,fn):
        """
        Saves an image of the current state of the scene.

        Parameters
        ----------
        fn : string
            The filename to save the image under.

        Returns
        -------
        None.

        """
        #iTHOR provides a BGR image to use direct with CV2
        cv2.imwrite(os.path.join(self.image_dir,fn),self.controller.last_event.cv2img);
        
    def hide_asset(self,name):
        """
        Puts the named asset back in its home position.

        Parameters
        ----------
        name : string
            The name of the asset to move.

        Returns
        -------
        None.

        """
        items = Items();
        #Get the home position of the asset
        pos = items.get_home_position(name);
        #Get the objectId using the asset name
        object_id = self.name_to_object_id(name);
        #Place the object out of sight
        self.controller.step(action="PlaceObjectAtPoint",
                             objectId=object_id,
                             position=pos,
                             rotation={'x':0,'y':0,'z':0});
        
    def stop(self):
        """
        Stops the underlying iTHOR controller.

        Returns
        -------
        None.

        """
        self.controller.stop();