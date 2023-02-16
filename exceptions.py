#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 14:44:05 2023

@author: dan
"""

class DuplicateAssetError(Exception):
    pass;
    
class MissingAssetError(Exception):
    pass;

class GridCoordinateError(Exception):
    pass;
    
class SlotFullError(Exception):
    pass;
    
class NoObjectError(Exception):
    pass;
    
class NoMatError(Exception):
    pass;
    
class UnsupportedSystemError(Exception):
    pass;
    
class MissingBuildFileError(Exception):
    pass;