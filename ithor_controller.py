#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 10:47:11 2023

@author: dan
"""

from ai2thor.controller import Controller;
from table import Table;
import cv2;

class Ithor_Controller:
    
    def __init__(self,height,width,local_exec_path,field_of_view,image_dir):
        self.controller = Controller(height=height,
                                width=width,
                                local_executable_path=local_exec_path,
                                fieldOfView=field_of_view,
                                snapToGrid=False);
        self.table = Table();
    
    def init_scene(self,pos,rot,horizon):
        self.controller.step(action="Teleport",
                             position=dict(x=pos[0],y=pos[1],z=pos[2]),
                             rotation=dict(x=0,y=rot,z=0),
                             horizon=horizon,
                             forceAction=True);
        
    def name_to_object_id(self,name):
        objs = self.controller.last_event.metadata['objects'];
        named_objs = [o for o in objs if o['name'] == name];
        if len(named_objs) == 1:
            return named_objs[0]['objectId'];
        else:
            return None;
        
    def pickup(self,name):
        object_id = self.name_to_object_id(name, self.controller.last_event);
        self.controller.step(action="PickupObject",objectId=object_id);
        
    def place_object(self,name,x,y,mat=True):
        pos = self.table.grid_to_coords(x,y,mat);
        print(pos);
        object_id = self.name_to_object_id(name);
        self.controller.step(action="PlaceObjectAtPoint",
                             objectId=object_id,
                             position=pos,
                             rotation={'x':0,'y':0,'z':0});
        print(self.controller.last_event);
        
    def save_img(self,path):
        cv2.imwrite(path,self.controller.last_event.cv2img);