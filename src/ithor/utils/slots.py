from exceptions import NoObjectError
from exceptions import SlotFullError

class Slot:
    def __init__(self, x, y, mat):
        """
        Constructor for new slots.

        Parameters
        ----------
        x : int
            The horizontal grid coordinate of this slot.
        y : int
            The vertical grid coordinate of this slot.
        mat : string
            The mat (if any) to add to this slot.

        Returns
        -------
        A new slot (possibly with a mat).

        """
        self.x = x
        self.y = y
        self.mat = mat
        self.object = None

    def check_empty(self, name):
        """
        Checks if the slot is empty for adding a new object.

        Parameters
        ----------
        name : string
            The name of the object to add to the slot.

        Raises
        ------
        SlotFullError
            Will raise a SlotFullError if the slot is already full.

        Returns
        -------
        bool
            Returns True if the slot is empty.

        """
        if self.has_object():
            raise SlotFullError(
                "Cannot place object ({}) here as there is already an object ({}) in this slot ({},{}).".format(
                    name, self.mat, self.x, self.y
                )
            )
        if self.is_full():
            raise SlotFullError(
                "Cannot place object ({}) here as there is already a mat ({}) and an object ({}) in this slot ({},{}).".format(
                    name, self.mat, self.object, self.x, self.y
                )
            )
        return True

    def place_object(self, name):
        """
        Place an object into this slot.

        Parameters
        ----------
        name : string
            The object to place into this slot.

        Raises
        ------
        SlotFullError
            Will raise a SlotFullError if the slot is already full.

        Returns
        -------
        None.

        """
        # Check to see if the slot is empty first
        self.check_empty(name)
        # If no exception thrown, add the object
        self.object = name

    def remove_object(self):
        """
        Remove the object in this slot.

        Raises
        ------
        NoObjectError
            Will raise a NoObjectError if the slot is already empty.

        Returns
        -------
        None.

        """
        if not self.has_object():
            raise NoObjectError(
                "There is no object to remove from this slot ({},{})".format(
                    self.x, self.y
                )
            )
        else:
            self.object = None

    def is_empty(self):
        """
        True if there is nothing in this slot.

        Returns
        -------
        bool
            True if empty, False if there is a mat or an object.

        """
        if self.mat is None and self.object is None:
            return True
        else:
            return False

    def has_mat(self):
        """
        True if there is a mat in this slot.

        Returns
        -------
        bool
            True if there is a mat, False if slot is empty or only has an object.

        """
        if self.mat is not None:
            return True
        else:
            return False

    def has_object(self):
        """
        True if the slot has an object.

        Returns
        -------
        bool
            True if slot has an object, False if there is no object.

        """
        if self.object is not None:
            return True
        else:
            return False

    def is_full(self):
        """
        True if slot has both an object and a mat.

        Returns
        -------
        bool
            True if slot has an object and a mat, False if either/both is missing.

        """
        if self.mat is not None and self.object is not None:
            return True
        else:
            return False
