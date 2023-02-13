#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 12:46:11 2023

@author: dan
"""
TOP_MARGIN = 0.035;
SIDE_MARGIN = 0.0075;
VERTICAL_PAD = 0.03;
HORIZONTAL_PAD = 0.007;
SLOT_DIM = 0.33;
LEFT_EDGE = -0.001 - (2.03 / 2);
TOP_EDGE = -0.079 - (1.12 / 2);
VERTICAL_SLOTS = 3;
HORIZONTAL_SLOTS = 6;
TABLE_HEIGHT = 1.6;
OBJECT_HEIGHT = 1.3;
 

class Table:
    
    def grid_to_coords(self,x,y,mat=True):
        #X is vertical position, Y is height, Z is horizontal position
        if x > HORIZONTAL_SLOTS or x < 0:
            return None;
        if y > VERTICAL_SLOTS or y < 0:
            return None;
        X = TOP_EDGE + TOP_MARGIN + y*SLOT_DIM + y*VERTICAL_PAD + (SLOT_DIM / 2);
        Y = TABLE_HEIGHT if mat else OBJECT_HEIGHT;
        Z = LEFT_EDGE + SIDE_MARGIN + x*SLOT_DIM + x*HORIZONTAL_PAD + (SLOT_DIM / 2);
        return {'x': X, 'y': Y, 'z': Z};
    
    