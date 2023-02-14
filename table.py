#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 12:46:11 2023

@author: dan
"""
#The areas at the top/bottom and left/right to keep clear
TOP_MARGIN = 0.035;
SIDE_MARGIN = 0.0075;
#The padding between the grid squares to keep clear
VERTICAL_PAD = 0.03;
HORIZONTAL_PAD = 0.007;
#The size of each grid square in both dimensions
SLOT_DIM = 0.33;
#The iTHOR coordinates of the left/top edges of the table
LEFT_EDGE = -0.001 - (2.03 / 2);
TOP_EDGE = -0.079 - (1.12 / 2);
#The number of slots in the grid
VERTICAL_SLOTS = 3;
HORIZONTAL_SLOTS = 6;
#The iTHOR Y value for the table height
TABLE_HEIGHT = 1.1471;
 

class GridCoordinateError(Exception):
    pass;

class Table:
    
    #def __init__(self)
    
    def grid_to_coords(self,x,y):
        """
        Converts grid coordinates to iTHOR coordinates.

        Parameters
        ----------
        x : int
            The horizontal grid coordinate.
        y : TYPE
            The vertical grid coordinate.

        Returns
        -------
        dict
            A dictionary of coordinates in iTHOR format.

        """
        #Cannot give coordinates if outside of the grid
        if x > HORIZONTAL_SLOTS or x < 0:
            raise GridCoordinateError("{} is out of bounds for {} horizontal slots.".format(x,HORIZONTAL_SLOTS));
        if y > VERTICAL_SLOTS or y < 0:
            raise GridCoordinateError("{} is out of bounds for {} vertical slots.".format(y,VERTICAL_SLOTS));
        #Two slots interfere with the agent object and can't be used
        if y == 2 and (x == 2 or x == 3):
            raise GridCoordinateError("(2,2) and (3,2) are reserved slots and cannot be used.")
        #X is vertical position in iTHOR coordinates
        X = TOP_EDGE + TOP_MARGIN + y*SLOT_DIM + y*VERTICAL_PAD + (SLOT_DIM / 2);
        #Y is height
        Y = TABLE_HEIGHT;
        #Z is horizontal position
        Z = LEFT_EDGE + SIDE_MARGIN + x*SLOT_DIM + x*HORIZONTAL_PAD + (SLOT_DIM / 2);
        return {'x': X, 'y': Y, 'z': Z};
    
    