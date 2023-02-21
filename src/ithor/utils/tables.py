from slots import Slot
from exceptions import DuplicateAssetError
from exceptions import GridCoordinateError
from exceptions import NoMatError

# The areas at the top/bottom and left/right to keep clear
TOP_MARGIN = 0.035
SIDE_MARGIN = 0.0075
# The padding between the grid squares to keep clear
VERTICAL_PAD = 0.03
HORIZONTAL_PAD = 0.007
# The size of each grid square in both dimensions
SLOT_DIM = 0.33
# The iTHOR coordinates of the left/top edges of the table
LEFT_EDGE = -0.001 - (2.03 / 2)
TOP_EDGE = -0.079 - (1.12 / 2)
# The number of slots in the grid
VERTICAL_SLOTS = 3
HORIZONTAL_SLOTS = 6
# The iTHOR Y value for the table height
TABLE_HEIGHT = 1.1471


class Table:
    def __init__(self, mats, objects):
        """
        Initalises table with mats in the specified positions.

        Parameters
        ----------
        mats : list of list of string
            A 6 by 3 list of mat names.

        objects : list of list of string
            A 6 by 3 list of object names.

        Raises
        ------
        GridCoordinateError
            Will raise a GridCoordinateError if the mats list is not H x V.

        DuplicateAssetError
            Raises DuplicateAssetError if an asset name appears more than once.

        NoMatError
            Raises NoMatError if a goal object is placed where there is no mat.

        Returns
        -------
        A newly initalised Table with mats in specified positions.

        """
        # Check if mats have been placed in the reserved slots
        if mats[2][2] is not None or mats[3][2] is not None:
            raise GridCoordinateError(
                "(2,2) and (3,2) are reserved slots and cannot be used."
            )
        # Check the dimensions of the mats list
        if len(mats) != HORIZONTAL_SLOTS:
            raise GridCoordinateError(
                "List of mats was {} wide, it should be {} wide.".format(
                    len(mats), HORIZONTAL_SLOTS
                )
            )
        if not all([len(s) == VERTICAL_SLOTS for s in mats]):
            raise GridCoordinateError(
                "List of mats must be {} tall".format(VERTICAL_SLOTS)
            )

        # Create a new grid of slots and put mats in specified slots
        self.grid = []
        for x in range(HORIZONTAL_SLOTS):
            self.grid.append([])
            for y in range(VERTICAL_SLOTS):
                self.grid[x].append(Slot(x, y, mats[x][y]))
                if objects[x][y] is not None:
                    go = objects[x][y]
                    if mats[x][y] is None:
                        raise NoMatError(
                            "Tried to place {} at position ({},{}) but there's no mat there.".format(
                                go, x, y
                            )
                        )
                    self.grid[x][y].place_object(go)
        # Check that there are no assests used more than once
        self.check_for_duplicates()

    def check_for_duplicates(self):
        """
        Checks if any of the assests have been listed more than once.

        Raises
        ------
        DuplicateAssetError
            Raises DuplicateAssetError if an asset name appears more than once.

        Returns
        -------
        None.

        """
        assets = []
        for column in self.grid:
            for slot in column:
                if slot.has_object():
                    assets.append(slot.object)
                if slot.has_mat():
                    assets.append(slot.mat)
        if len(assets) != len(set(assets)):
            raise DuplicateAssetError("An asset has been listed more than once.")

    def grid_to_coords(self, x, y):
        """
        Converts grid coordinates to iTHOR coordinates.

        Parameters
        ----------
        x : int
            The horizontal grid coordinate.
        y : TYPE
            The vertical grid coordinate.

        Raises
        ------
        GridCoordinateError
            Will raise a GridCoordinateError if specified coordinates is out of bounds.


        Returns
        -------
        dict
            A dictionary of coordinates in iTHOR format.

        """
        # Cannot give coordinates if outside of the grid
        if x > HORIZONTAL_SLOTS or x < 0:
            raise GridCoordinateError(
                "{} is out of bounds for {} horizontal slots.".format(
                    x, HORIZONTAL_SLOTS
                )
            )
        if y > VERTICAL_SLOTS or y < 0:
            raise GridCoordinateError(
                "{} is out of bounds for {} vertical slots.".format(y, VERTICAL_SLOTS)
            )
        # Two slots interfere with the agent object and can't be used
        if y == 2 and (x == 2 or x == 3):
            raise GridCoordinateError(
                "(2,2) and (3,2) are reserved slots and cannot be used."
            )
        # X is vertical position in iTHOR coordinates
        X = TOP_EDGE + TOP_MARGIN + y * SLOT_DIM + y * VERTICAL_PAD + (SLOT_DIM / 2)
        # Y is height
        Y = TABLE_HEIGHT
        # Z is horizontal position
        Z = LEFT_EDGE + SIDE_MARGIN + x * SLOT_DIM + x * HORIZONTAL_PAD + (SLOT_DIM / 2)
        return {"x": X, "y": Y, "z": Z}

    def get_empty_slots_list():
        """
        Returns an empty list of lists for specifying mat/object positions.

        Returns
        -------
        list of list
            An empty list of list for specifying mat/object positions.
        """
        mats = []
        for x in range(HORIZONTAL_SLOTS):
            mats.append([])
            for y in range(VERTICAL_SLOTS):
                mats[-1].append(None)
        return mats
    
