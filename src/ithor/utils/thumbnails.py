import os

import cv2
import numpy as np
import random

from ithor.utils.exceptions import (
    ExistingThumbnailFolderError,
    MissingThumbnailsError,
)
from ithor.utils.items import Items

THUMB_DIM = 200
# The (square) thumbnail size
PAD = 20
# The padding between elements in the grid
X_CROP_START = 425
# The left edge of the scene to crop when creating thumbnails
Y_CROP_START = 600
# The top edge of the scene to crop when creating thumbnails
FONT_FACE = cv2.FONT_HERSHEY_COMPLEX_SMALL
# The font to use
TEXT_SCALE = 2
# The font size for the main text labels
LABEL_SCALE = 1
# The font size for the individual asset labels
FONT_THICKNESS = 1
# The font thickness to use
FONT_COLOUR = (0, 0, 0)
# The colour for the labels (set to black)
TEXT_HEIGHT = 39
# The height of the main text labels
LABEL_HEIGHT = 20
# The height of the smaller asset labels


HEIGHT = 1200
WIDTH = 1600
HORIZONTAL_MARGIN = 75
HORIZONTAL_PAD = 50
VERTICAL_MARGIN = 0
TEXT_PAD = 4
LABEL_PAD = 2

class Thumbnails:
    def __init__(self, image_dir, controller=None):
        """
        Initalises a Thumbnails object, attempting to create the thumbnails if they don't exist.

        Parameters
        ----------
        image_dir : string
            The base directory for images.
        controller : IthorController, optional
            A IthorController for a blank scene to create new thumbnails. The default is None.

        Raises
        ------
        MissingThumbnailsError
            Raises a MissingThumbnailsError if the thumbnails don't exist already and no controller has been provided to create them.

        Returns
        -------
        A initialised Thumbnails object.

        """
        self.items = Items()
        # Get the metadata for the items
        # Thumbnails directory is just a subfolder of the main images directory
        self.thumb_dir = os.path.join(image_dir, "thumbnails")

        # Check to see if the thumbnails folder exists
        if not os.path.exists(self.thumb_dir):
            # Need a controller to create thumbnails if they don't already exist
            if controller is None:
                raise MissingThumbnailsError(
                    "Thumbnail folder not found. Provide a controller for a blank iTHOR scene to generate thumbnails."
                )
            else:
                # If they don't exist and a controller is provided, create a new set of thumbnails
                self.generate_thumbnails(controller)

        # Read in the image data for the thumbnails
        self.imgs = {}
        for fn in os.listdir(self.thumb_dir):
            self.imgs[fn[:-4]] = cv2.imread(os.path.join(self.thumb_dir, fn))

    def show_grid(self, grid):
        """
        A helper method to show a grid image for testing. Press any key to close the window (closing it manually will crash CV2).

        Parameters
        ----------
        grid : numpy.array
            A numpy array containing the image data for a grid to display.

        Returns
        -------
        None.

        """
        cv2.imshow("Thumbnail Grid", grid)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def generate_grid(self, leader_table, follower_table, display_names=False):
        """
        Generates a grid of objects and mats in the scene.

        Parameters
        ----------
        objects : list of string
            A list of the names of the objects used in the scene.
        mats : list of string
            A list of the names of the mats used in the scene.
        display_names : bool, optional
            If True, the labels will be the object names, if False, objects will be assigned a number and mats will be assigned a letter. The default is False.

        Returns
        -------
        numpy.array
            A numpy array with the image data for the grid.
        """
        # Get the various dimensions needed to set up the grid according to the number of items
        #self.get_grid_size(objects, mats)
        # Create a blank image array and set the pixels to white by default
        #grid = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        
        grid = np.ones((HEIGHT,WIDTH,3),dtype=np.uint8) * 255
        
        self.mat_text_pos = (HORIZONTAL_MARGIN, VERTICAL_MARGIN + TEXT_HEIGHT)
        self.obj_text_pos = (
            HORIZONTAL_MARGIN,
            VERTICAL_MARGIN
            + TEXT_HEIGHT * 2 + TEXT_PAD
            + (THUMB_DIM + LABEL_HEIGHT + LABEL_PAD) * 3)

        # Add text for the objects and mats using the larger font size
        cv2.putText(
            img=grid,
            text="Mats:",
            org=self.mat_text_pos,
            fontFace=FONT_FACE,
            fontScale=TEXT_SCALE,
            color=FONT_COLOUR,
            thickness=FONT_THICKNESS
        )
        cv2.putText(
            img=grid,
            text="Objects:",
            org=self.obj_text_pos,
            fontFace=FONT_FACE,
            fontScale=TEXT_SCALE,
            color=FONT_COLOUR,
            thickness=FONT_THICKNESS
        )
        
        for x,column in enumerate(leader_table.grid):
            for y,slot in enumerate(column):
                if leader_table.grid[x][y].has_mat():
                    mat = slot.mat
                    left, top = self.mat_coords_to_pixels(x, y)
                    right = left + THUMB_DIM
                    bottom = top + THUMB_DIM
        
                    grid[top:bottom, left:right] = self.imgs[mat]
                    if display_names:
                        label = mat
                    else:
                        label = self.items.get_asset(mat)["slurk_id"]
                    cv2.putText(
                        img=grid,
                        text=label,
                        org=(left, bottom + LABEL_HEIGHT),
                        fontFace=FONT_FACE,
                        fontScale=LABEL_SCALE,
                        color=FONT_COLOUR,
                        thickness=FONT_THICKNESS
            )
                    
        objects = set()
        for x,column in enumerate(leader_table.grid):
            for y,slot_l in enumerate(column):           
                slot_f = follower_table.grid[x][y]
                if slot_l.has_object():
                    objects.add(slot_l.object)
                if slot_f.has_object():
                    objects.add(slot_f.object)
                    
        items = Items()
        all_objs = [obj['name'] for obj in items.objects]
        while(len(objects) < 12):
            objects.add(random.choice(all_objs))
        
        objects = list(objects)
        random.shuffle(objects)
        
        for i,obj in enumerate(objects):
            left, top = self.obj_index_to_pixels(i)
            right = left + THUMB_DIM
            bottom = top + THUMB_DIM

            grid[top:bottom, left:right] = self.imgs[obj]
            if display_names:
                label = obj
            else:
                label = self.items.get_asset(obj)["slurk_id"]
            cv2.putText(
                img=grid,
                text=label,
                org=(left, bottom + LABEL_HEIGHT),
                fontFace=FONT_FACE,
                fontScale=LABEL_SCALE,
                color=FONT_COLOUR,
                thickness=FONT_THICKNESS)
        return grid

    def mat_coords_to_pixels(self,x,y):
        xp = HORIZONTAL_MARGIN + (THUMB_DIM + HORIZONTAL_PAD) * x
        yp = VERTICAL_MARGIN + (TEXT_HEIGHT + TEXT_PAD) + (THUMB_DIM + LABEL_HEIGHT + LABEL_PAD) * y
        return (xp,yp)
    
    def obj_index_to_pixels(self,i):
        xp = HORIZONTAL_MARGIN + (THUMB_DIM + HORIZONTAL_PAD) * (i % 6)
        yp = VERTICAL_MARGIN + (TEXT_HEIGHT + TEXT_PAD) * 2 + (THUMB_DIM + LABEL_HEIGHT + LABEL_PAD) * (3 + i//6)
        return (xp,yp)

    def generate_thumbnails(self, blank_scene_controller):
        """
        Generates a new set of thumbnail images.

        Parameters
        ----------
        blank_scene_controller : IthorController
            An IthorController for a blank scene.

        Raises
        ------
        ExistingThumbnailFolderError
            Raises ExistingThumbnailFolderError if there is already a thumbnail folder to prevent overwriting or leaving old thumbnails.

        Returns
        -------
        None.

        """
        # Try making the thumbnail folder
        try:
            os.makedirs(self.thumb_dir)
        except FileExistsError:
            # Throw an error if the folder already exists (even if it's empty)
            raise ExistingThumbnailFolderError(
                "A thumbnail folder already exists, please delete it and try again."
            )

        # Go through all the assets and generate a thumbnail
        for asset in self.items.assets:
            name = asset["name"]
            # Place the asset in the centre of the table
            blank_scene_controller.place_asset(name, 2, 1)
            # Get an image of the whole scene
            img = blank_scene_controller.controller.last_event.cv2img
            # Crop the image to just the item
            cropped_img = img[
                X_CROP_START : (X_CROP_START + THUMB_DIM),
                Y_CROP_START : (Y_CROP_START + THUMB_DIM),
            ]
            # Write the image to file
            cv2.imwrite(
                os.path.join(self.thumb_dir, "{}.png".format(name)), cropped_img
            )
            # Move the asset off the table, leaving it blank
            blank_scene_controller.hide_asset(name)
        # Stop the iTHOR scene
        blank_scene_controller.stop()
