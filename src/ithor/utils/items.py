from ithor.utils.exceptions import DuplicateAssetError, MissingAssetError

assets = [{'name': 'Square1',
  'slurk_id': '#A',
  'colour': 'Blue',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 3.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Square2',
  'slurk_id': '#B',
  'colour': 'Blue',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 4.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Square3',
  'slurk_id': '#C',
  'colour': 'Red',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 4.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Square4',
  'slurk_id': '#D',
  'colour': 'Red',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 5.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Square5',
  'slurk_id': '#E',
  'colour': 'Yellow',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 5.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Square6',
  'slurk_id': '#F',
  'colour': 'Yellow',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 6.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Square7',
  'slurk_id': '#G',
  'colour': 'Orange',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 6.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Square8',
  'slurk_id': '#H',
  'colour': 'Orange',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 7.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Square9',
  'slurk_id': '#I',
  'colour': 'Green',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 7.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Square10',
  'slurk_id': '#J',
  'colour': 'Green',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 8.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Square11',
  'slurk_id': '#K',
  'colour': 'Violet',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 8.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Square12',
  'slurk_id': '#L',
  'colour': 'Indigo',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 9.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Square13',
  'slurk_id': '#M',
  'colour': 'Iris',
  'is_mat': True,
  'home_pos': {'x': -2.0, 'y': 1.0, 'z': 9.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle1',
  'slurk_id': '#N',
  'colour': 'Blue',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 3.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle2',
  'slurk_id': '#O',
  'colour': 'Blue',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 4.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle3',
  'slurk_id': '#P',
  'colour': 'Red',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 4.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle4',
  'slurk_id': '#Q',
  'colour': 'Red',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 5.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle5',
  'slurk_id': '#R',
  'colour': 'Yellow',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 5.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle6',
  'slurk_id': '#S',
  'colour': 'Yellow',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 6.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle7',
  'slurk_id': '#T',
  'colour': 'Orange',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 6.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle8',
  'slurk_id': '#U',
  'colour': 'Orange',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 7.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle9',
  'slurk_id': '#V',
  'colour': 'Green',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 7.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle10',
  'slurk_id': '#W',
  'colour': 'Green',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 8.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle11',
  'slurk_id': '#X',
  'colour': 'Violet',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 8.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle12',
  'slurk_id': '#Y',
  'colour': 'Indigo',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 9.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Circle13',
  'slurk_id': '#Z',
  'colour': 'Iris',
  'is_mat': True,
  'home_pos': {'x': -1.5, 'y': 1.0, 'z': 9.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Apple1',
  'slurk_id': '#1',
  'colour': 'Red',
  'is_mat': False,
  'home_pos': {'x': -1.0, 'y': 1.0, 'z': 3.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Apple1Slice',
  'slurk_id': '#2',
  'colour': 'Red',
  'is_mat': False,
  'home_pos': {'x': -1.0, 'y': 1.0, 'z': 4.0},
  'home_rot': {'x': 0.0, 'y': 190.0, 'z': 0.0}},
 {'name': 'Apple2',
  'slurk_id': '#3',
  'colour': 'Green',
  'is_mat': False,
  'home_pos': {'x': -1.0, 'y': 1.0, 'z': 4.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Apple2Slice',
  'slurk_id': '#4',
  'colour': 'Green',
  'is_mat': False,
  'home_pos': {'x': -1.0, 'y': 1.0, 'z': 5.0},
  'home_rot': {'x': 0.0, 'y': 190.0, 'z': 0.0}},
 {'name': 'Apple3',
  'slurk_id': '#5',
  'colour': 'Yellow',
  'is_mat': False,
  'home_pos': {'x': -1.0, 'y': 1.0, 'z': 5.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Apple3Slice',
  'slurk_id': '#6',
  'colour': 'Yellow',
  'is_mat': False,
  'home_pos': {'x': -1.0, 'y': 1.0, 'z': 6.0},
  'home_rot': {'x': 0.0, 'y': 190.0, 'z': 0.0}},
 {'name': 'Cup1',
  'slurk_id': '#7',
  'colour': 'Green',
  'is_mat': False,
  'home_pos': {'x': -0.5, 'y': 1.0, 'z': 3.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Cup2',
  'slurk_id': '#8',
  'colour': 'Orange',
  'is_mat': False,
  'home_pos': {'x': -0.5, 'y': 1.0, 'z': 4.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Bowl1',
  'slurk_id': '#9',
  'colour': 'Blue',
  'is_mat': False,
  'home_pos': {'x': 0.0, 'y': 1.0, 'z': 3.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Bowl2',
  'slurk_id': '#10',
  'colour': 'Brown',
  'is_mat': False,
  'home_pos': {'x': -0.0, 'y': 1.0, 'z': 4.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Bowl3',
  'slurk_id': '#11',
  'colour': 'Black',
  'is_mat': False,
  'home_pos': {'x': -0.0, 'y': 1.0, 'z': 4.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Bread1',
  'slurk_id': '#12',
  'colour': 'White',
  'is_mat': False,
  'home_pos': {'x': 0.5, 'y': 1.0, 'z': 3.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Bread1Slice',
  'slurk_id': '#13',
  'colour': 'White',
  'is_mat': False,
  'home_pos': {'x': 0.5, 'y': 1.0, 'z': 4.0},
  'home_rot': {'x': 90.0, 'y': 0.0, 'z': 90.0}},
 {'name': 'Bread2',
  'slurk_id': '#14',
  'colour': 'Brown',
  'is_mat': False,
  'home_pos': {'x': 0.5, 'y': 1.0, 'z': 4.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Bread2Slice',
  'slurk_id': '#15',
  'colour': 'Brown',
  'is_mat': False,
  'home_pos': {'x': 0.5, 'y': 1.0, 'z': 5.0},
  'home_rot': {'x': 90.0, 'y': 0.0, 'z': 90.0}},
 {'name': 'Egg1',
  'slurk_id': '#16',
  'colour': 'Brown',
  'is_mat': False,
  'home_pos': {'x': 1.0, 'y': 1.0, 'z': 3.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Egg2',
  'slurk_id': '#17',
  'colour': 'White',
  'is_mat': False,
  'home_pos': {'x': 1.0, 'y': 1.0, 'z': 4.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Pan1',
  'slurk_id': '#18',
  'colour': 'Silver',
  'is_mat': False,
  'home_pos': {'x': 1.5, 'y': 1.0, 'z': 3.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Pan2',
  'slurk_id': '#19',
  'colour': 'Black',
  'is_mat': False,
  'home_pos': {'x': 1.5, 'y': 1.0, 'z': 4.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Plate1',
  'slurk_id': '#20',
  'colour': 'White',
  'is_mat': False,
  'home_pos': {'x': 2.0, 'y': 1.0, 'z': 3.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Plate2',
  'slurk_id': '#21',
  'colour': 'Blue',
  'is_mat': False,
  'home_pos': {'x': 2.0, 'y': 1.0, 'z': 4.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Vase1',
  'slurk_id': '#22',
  'colour': 'Red',
  'is_mat': False,
  'home_pos': {'x': 2.5, 'y': 1.0, 'z': 3.5},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
 {'name': 'Vase2',
  'slurk_id': '#23',
  'colour': 'Yellow',
  'is_mat': False,
  'home_pos': {'x': 2.5, 'y': 1.0, 'z': 4.0},
  'home_rot': {'x': 0.0, 'y': 0.0, 'z': 0.0}}]


class Items:
    def __init__(self):
        """
        Constructor for asset list.

        Returns
        -------
        A wrapper object for the assets list.

        """
        self.assets = assets
        self.objects = [a for a in assets if not a["is_mat"]]
        self.mats = [a for a in assets if a["is_mat"]]

    def get_asset(self, name):
        """
        Gets the named asset from the asset list.

        Parameters
        ----------
        name : string
            The name of the asset to retrieve.

        Raises
        ------
        DuplicateAssetError
            Raises a DuplicateAssetError if the asset name appears more than once in the asset list.
        MissingAssetError
            Raises a Missing AssetError if the asset name does not appear in the asset list.

        Returns
        -------
        dict
            Returns the dictionary for the asset.

        """
        named_assets = [a for a in assets if a["name"] == name]
        if len(named_assets) > 1:
            raise DuplicateAssetError(
                "More than one asset in the asset list has the name {}.".format(name)
            )
        if len(named_assets) == 0:
            raise MissingAssetError("No asset found with the name {}.".format(name))
        return named_assets[0]

    def is_object(self, name):
        """
        True if the named asset is an object.

        Parameters
        ----------
        name : string
            The name of the asset to check.

        Raises
        ------
        DuplicateAssetError
            Raises a DuplicateAssetError if the asset name appears more than once in the asset list.
        MissingAssetError
            Raises a Missing AssetError if the asset name does not appear in the asset list.


        Returns
        -------
        bool
            True if the asset is an object, False if it is a mat.

        """
        return not self.get_asset(name)["is_mat"]

    def is_mat(self, name):
        """
        True if the named asset is a mat.

        Parameters
        ----------
        name : string
            The name of the asset to check.

        Raises
        ------
        DuplicateAssetError
            Raises a DuplicateAssetError if the asset name appears more than once in the asset list.
        MissingAssetError
            Raises a Missing AssetError if the asset name does not appear in the asset list.


        Returns
        -------
        bool
            True if the asset is a mat, False if it is an object.

        """
        return self.get_asset(name)["is_mat"]

    def get_colour(self, name):
        """
        Returns the colour of the named asset.

        Parameters
        ----------
        name : string
            The name of the asset to check.

        Raises
        ------
        DuplicateAssetError
            Raises a DuplicateAssetError if the asset name appears more than once in the asset list.
        MissingAssetError
            Raises a Missing AssetError if the asset name does not appear in the asset list.


        Returns
        -------
        string
            The colour of the named asset.

        """
        return self.get_asset(name)["colour"]

    def get_home_position(self, name):
        """
        Returns the home position of the named asset.

        Parameters
        ----------
        name : string
            The name of the asset to check.

        Raises
        ------
        DuplicateAssetError
            Raises a DuplicateAssetError if the asset name appears more than once in the asset list.
        MissingAssetError
            Raises a Missing AssetError if the asset name does not appear in the asset list.


        Returns
        -------
        dict of float
            The home position of the named asset.

        """
        return self.get_asset(name)["home_pos"]
    
    def get_home_rotation(self,name):
        """
        Returns the home rotation of the named asset.

        Parameters
        ----------
        name : string
            The name of the asset to check.

        Raises
        ------
        DuplicateAssetError
            Raises a DuplicateAssetError if the asset name appears more than once in the asset list.
        MissingAssetError
            Raises a Missing AssetError if the asset name does not appear in the asset list.


        Returns
        -------
        dict of float
            The home rotation of the named asset.

        """
        return self.get_asset(name)["home_rot"]

    def get_name_by_slurkid(self, slurk_id):
        name = [a["name"] for a in assets if a["slurk_id"] == slurk_id]
        return name[0]
