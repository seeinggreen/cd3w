import os

from datetime import date
import json

import cv2
from ai2thor.controller import Controller
from ithor.utils.build import get_local_build_path
from ithor.utils.exceptions import DuplicateAssetError, MissingAssetError
from ithor.utils.items import Items
from ithor.utils.table import Table

import base64

LOCAL_BUILD_PATH = get_local_build_path()


class IthorController:
    def __init__(
        self,
        height=1200,
        width=1600,
        local_exec_path=LOCAL_BUILD_PATH,
        field_of_view=120,
    ):
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

        Returns
        -------
        An Ithor_Controller wrapper object.

        """

        self.table = None

        # Set up a standard iTHOR controller
        self.controller = Controller(
            height=height,
            width=width,
            local_executable_path=local_exec_path,
            fieldOfView=field_of_view,
            snapToGrid=False,
        )
        self.items = Items()

    def init_scene(self, pos, rot, horizon):
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

        # Physically move the agent to the specified position
        self.controller.step(
            action="Teleport",
            position={"x": pos[0], "y": pos[1], "z": pos[2]},
            rotation={"x": 0, "y": rot, "z": 0},
            horizon=horizon,
            forceAction=True,
        )

    def name_to_object_id(self, name):
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
        # Take the metadata from the last event to ensure it's up to date
        objs = self.controller.last_event.metadata["objects"]
        # Get all the objects with that asset name
        named_objs = [o for o in objs if o["name"] == name]
        # Should be a singleton list, so return the objectId of the first entry
        if len(named_objs) > 1:
            raise DuplicateAssetError(
                f"{len(named_objs)} objects were found for {name}, expected just one."
            )
        if len(named_objs) == 0:
            raise MissingAssetError(f"Could not find the asset called {name}.")
        return named_objs[0]["objectId"]

    def pickup(self, name):
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
        object_id = self.name_to_object_id(name)
        # Objects should be in front of the agent before calling this method
        self.controller.step(action="PickupObject", objectId=object_id)
        grid = self.table.grid
        for column in grid:
            for slot in column:
                if slot.object == name:
                    slot.object = None

    def place_assets(self, config):
        """
        Places all assets specified in the table grid in their locations.

        Parameters
        ----------
        config : dict
            The scene config (mats / objects in grid slots)

        Returns
        -------
        None.

        """
        if config == None:
            self.table = Table(
                Table.get_empty_slots_list(), Table.get_empty_slots_list()
            )
        else:
            self.table = Table(config["mats"], config["objects"])

        grid = self.table.grid
        for x, column in enumerate(grid):
            for y, slot in enumerate(column):
                if slot.has_mat():
                    self.place_asset_at_location(slot.mat, x, y)
                if slot.has_object():
                    self.place_asset_at_location(slot.object, x, y)

    def place_asset_at_location(self, name, x, y):
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
        # Convert the grid coordinates to iTHOR coordinates (can raise GridCoordinateError)
        pos = self.table.grid_to_coords(x, y)
        # Get the objectId using the asset name
        object_id = self.name_to_object_id(name)
        # Place the object with no rotation
        self.controller.step(
            action="PlaceObjectAtPoint",
            objectId=object_id,
            position=pos,
            rotation=self.items.get_home_rotation(name),
        )

    def place_asset_at_empty_location(self, name):
        grid = self.table.grid
        asset_placed = False
        for x, column in enumerate(grid):
            if asset_placed:
                break
            for y, slot in enumerate(column):
                if asset_placed:
                    break
                if y == 2 and (x == 2 or x == 3):
                    continue
                if slot.is_empty():
                    slot.place_object(name)
                    self.place_asset_at_location(name, x, y)
                    asset_placed = True
                    print(f"{name} placed at {x}{y}")

    def place_object_on_mat(self, object_name, mat_name):
        grid = self.table.grid
        for x, column in enumerate(grid):
            for y, slot in enumerate(column):
                if slot.mat == mat_name:
                    slot.place_object(object_name)
                    self.place_asset_at_location(object_name, x, y)

    def snapshot_scene(self):
        """
        Returns
        -------
        A base64 encoded image url for the current state of the scene.

        """
        # iTHOR provides a BGR image to use direct with CV2
        _, buffer = cv2.imencode(".jpg", self.controller.last_event.cv2img)
        return f"data:image/jpg;base64,{base64.b64encode(buffer).decode()}"

    def hide_asset(self, name):
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
        # Get the objectId using the asset name
        object_id = self.name_to_object_id(name)
        # Place the object out of sight
        self.controller.step(
            action="PlaceObjectAtPoint",
            objectId=object_id,
            position=self.items.get_home_position(name),
            rotation=self.items.get_home_rotation(name),
        )
        for column in self.table.grid:
            for slot in column:
                if slot.object == name:
                    slot.remove_object()

    def stop(self):
        """
        Stops the underlying iTHOR controller.

        Returns
        -------
        None.

        """
        self.controller.stop()

    def save_table_state(self, level, variant, username):
        grid = self.table.grid
        mats = Table.get_empty_slots_list()
        objects = Table.get_empty_slots_list()
        for x, column in enumerate(grid):
            for y, slot in enumerate(column):
                if slot.has_mat():
                    mats[x][y] = slot.mat
                if slot.has_object():
                    objects[x][y] = slot.object

        config = {"mats": mats, "objects": objects}

        final_states_path = f"{os.path.abspath('')}/output/final_states/{level}_{variant}.json"
        existing_final_states = {str(date.today()): {username: config}}
        if os.path.exists(final_states_path):
            with open(final_states_path, encoding="utf-8") as json_file:
                existing_final_states = json.load(json_file)
            if str(date.today()) in existing_final_states:
                if username in existing_final_states[str(date.today())]:
                    existing_final_states[str(date.today())][username] = config
                else:
                    existing_final_states[str(date.today())].update({username: config})
            else:
                existing_final_states.update({str(date.today()): {username: config}})
        with open(
                final_states_path,
                "w",
            ) as outfile:
                json.dump(
                    existing_final_states,
                    outfile,
                )

    def get_current_table_items(self):
        grid = self.table.grid
        items = {"mats": [], "objects": []}
        for column in grid:
            for slot in column:
                if slot.has_mat():
                    items["mats"].append(slot.mat)
                if slot.has_object():
                    items["objects"].append(slot.object)

        return items
