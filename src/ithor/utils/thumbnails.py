import math
import os

import cv2
import numpy as np

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

    def generate_grid(self, objects, mats, display_names=False):
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
        self.get_grid_size(objects, mats)
        # Create a blank image array and set the pixels to white by default
        grid = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255

        # Add text for the objects and mats using the larger font size
        cv2.putText(
            img=grid,
            text="Objects:",
            org=self.obj_text_pos,
            fontFace=FONT_FACE,
            fontScale=TEXT_SCALE,
            color=FONT_COLOUR,
            thickness=FONT_THICKNESS,
        )
        cv2.putText(
            img=grid,
            text="Mats:",
            org=self.mat_text_pos,
            fontFace=FONT_FACE,
            fontScale=TEXT_SCALE,
            color=FONT_COLOUR,
            thickness=FONT_THICKNESS,
        )

        # Add the object thumbnails
        for i, obj in enumerate(objects):
            # Position gets calculated in the get_grid_size method
            left, top = self.obj_grid[i]
            # Right and bottom edges are just offsets according to the thumbnail size
            right = left + THUMB_DIM
            bottom = top + THUMB_DIM

            # Set the appropriate grid pixels to the thumbnail pixels
            grid[top:bottom, left:right] = self.imgs[obj]
            # Either keep the asset name as is or replace it with the slurk_id
            if display_names:
                label = obj
            else:
                label = self.items.get_asset(obj)["slurk_id"]
            # Add the text label in the smaller font size
            cv2.putText(
                img=grid,
                text=label,
                org=(left, bottom + LABEL_HEIGHT),
                fontFace=FONT_FACE,
                fontScale=LABEL_SCALE,
                color=FONT_COLOUR,
                thickness=FONT_THICKNESS,
            )

        # As above, but for mats
        for i, mat in enumerate(mats):
            left, top = self.mat_grid[i]
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
                thickness=FONT_THICKNESS,
            )

        return grid

    def get_grid_size(self, objects, mats):
        """
        Calculates the dimensions and positions of the grid according to the number of thumbnails.

        Parameters
        ----------
        objects : list
            A list of the objects (only the length of the list matters).
        mats : list
            A list of the mats (only the length of the list matters)..

        Returns
        -------
        None.

        """
        # We only care about how many thumbnails
        objects = len(objects)
        mats = len(mats)

        # Tile the thumbnails in rows of 4 when there is more than 4
        if objects >= 4 or mats >= 4:
            width = 4
        else:
            # If the number of thumbnails is less than 4, the grid width is the widest of the two
            width = max(objects, mats)

        # Convert to actual pixel widths with padding
        self.width = THUMB_DIM * width + PAD * (width + 1)

        # Calculate the number of (possibly incomplete) rows of 4 thumbnails
        obj_height = math.ceil(objects / 4)
        mat_height = math.ceil(mats / 4)

        # The total height of the grid, made up of the text, the images and the padding
        self.height = (
            PAD
            + TEXT_HEIGHT
            + (THUMB_DIM + LABEL_HEIGHT) * obj_height
            + PAD * (obj_height + 1)
        )
        self.height += (
            TEXT_HEIGHT
            + (THUMB_DIM + LABEL_HEIGHT) * mat_height
            + PAD * (mat_height + 1)
        )

        # The position of the two main text labels
        self.obj_text_pos = (PAD, PAD + TEXT_HEIGHT)
        self.mat_text_pos = (
            PAD,
            PAD
            + TEXT_HEIGHT * 2
            + PAD * (obj_height + 1)
            + (THUMB_DIM + LABEL_HEIGHT) * obj_height,
        )

        # Calculate the position of each of the object images
        self.obj_grid = []
        for o in range(objects):
            # Positions in coordinate space
            x = o % 4
            y = o // 4
            # Convert to actual pixel positions
            x = PAD * (x + 1) + THUMB_DIM * x
            y = self.obj_text_pos[1] + PAD * (y + 1) + (THUMB_DIM + LABEL_HEIGHT) * y
            # Save as a tuple
            self.obj_grid.append((x, y))

        # As above, but for mats
        self.mat_grid = []
        for m in range(mats):
            x = m % 4
            y = m // 4
            x = PAD * (x + 1) + THUMB_DIM * x
            y = self.mat_text_pos[1] + PAD * (y + 1) + (THUMB_DIM + LABEL_HEIGHT) * y
            self.mat_grid.append((x, y))

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
