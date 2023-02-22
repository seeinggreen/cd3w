from src.ithor.utils.exceptions import DuplicateAssetError
from src.ithor.utils.exceptions import MissingAssetError
import os
import cv2

assets = [
    {
        "name": "Square1",
        "slurk_id": "#A",
        "colour": "Blue",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 4.519999980926514,
        },
    },
    {
        "name": "Square2",
        "slurk_id": "#B",
        "colour": "Blue",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 4.794000148773193,
        },
    },
    {
        "name": "Square3",
        "slurk_id": "#C",
        "colour": "Red",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 5.071000099182129,
        },
    },
    {
        "name": "Square4",
        "slurk_id": "#D",
        "colour": "Red",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 5.341000080108643,
        },
    },
    {
        "name": "Square5",
        "slurk_id": "#E",
        "colour": "Yellow",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 5.611000061035156,
        },
    },
    {
        "name": "Square6",
        "slurk_id": "#F",
        "colour": "Yellow",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 5.88100004196167,
        },
    },
    {
        "name": "Square7",
        "slurk_id": "#G",
        "colour": "Orange",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 6.1519999504089355,
        },
    },
    {
        "name": "Square8",
        "slurk_id": "#H",
        "colour": "Orange",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 6.4120001792907715,
        },
    },
    {
        "name": "Square9",
        "slurk_id": "#I",
        "colour": "Green",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 6.681000232696533,
        },
    },
    {
        "name": "Square10",
        "slurk_id": "#J",
        "colour": "Green",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 6.936999797821045,
        },
    },
    {
        "name": "Square11",
        "slurk_id": "#K",
        "colour": "Violet",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 7.202000141143799,
        },
    },
    {
        "name": "Square12",
        "slurk_id": "#L",
        "colour": "Indigo",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 7.470000267028809,
        },
    },
    {
        "name": "Square13",
        "slurk_id": "#M",
        "colour": "Iris",
        "is_mat": True,
        "home_pos": {
            "x": -0.16599999368190765,
            "y": 1.014931559562683,
            "z": 7.742000579833984,
        },
    },
    {
        "name": "Circle1",
        "slurk_id": "#N",
        "colour": "Blue",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 4.519999980926514,
        },
    },
    {
        "name": "Circle2",
        "slurk_id": "#O",
        "colour": "Blue",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 4.798999786376953,
        },
    },
    {
        "name": "Circle3",
        "slurk_id": "#P",
        "colour": "Red",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 5.065999984741211,
        },
    },
    {
        "name": "Circle4",
        "slurk_id": "#Q",
        "colour": "Red",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 5.330999851226807,
        },
    },
    {
        "name": "Circle5",
        "slurk_id": "#R",
        "colour": "Yellow",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 5.60099983215332,
        },
    },
    {
        "name": "Circle6",
        "slurk_id": "#S",
        "colour": "Yellow",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 5.861000061035156,
        },
    },
    {
        "name": "Circle7",
        "slurk_id": "#T",
        "colour": "Orange",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 6.138000011444092,
        },
    },
    {
        "name": "Circle8",
        "slurk_id": "#U",
        "colour": "Orange",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 6.394000053405762,
        },
    },
    {
        "name": "Circle9",
        "slurk_id": "#V",
        "colour": "Green",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 6.664000034332275,
        },
    },
    {
        "name": "Circle10",
        "slurk_id": "#W",
        "colour": "Green",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 6.936999797821045,
        },
    },
    {
        "name": "Circle11",
        "slurk_id": "#X",
        "colour": "Violet",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 7.198999881744385,
        },
    },
    {
        "name": "Circle12",
        "slurk_id": "#Y",
        "colour": "Indigo",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 7.466000556945801,
        },
    },
    {
        "name": "Circle13",
        "slurk_id": "#Z",
        "colour": "Iris",
        "is_mat": True,
        "home_pos": {
            "x": 0.13899999856948853,
            "y": 1.014931559562683,
            "z": 7.734000205993652,
        },
    },
    {
        "name": "Apple1",
        "slurk_id": "#1",
        "colour": "Red",
        "is_mat": False,
        "home_pos": {
            "x": 0.4650000035762787,
            "y": 1.010363221168518,
            "z": 4.519000053405762,
        },
    },
    {
        "name": "Apple1Slice",
        "slurk_id": "#2",
        "colour": "Red",
        "is_mat": False,
        "home_pos": {
            "x": 0.4970000386238098,
            "y": 1.0333632230758667,
            "z": 4.843000411987305,
        },
    },
    {
        "name": "Apple2",
        "slurk_id": "#3",
        "colour": "Green",
        "is_mat": False,
        "home_pos": {
            "x": 0.4659999907016754,
            "y": 1.0103631019592285,
            "z": 5.067399978637695,
        },
    },
    {
        "name": "Apple2Slice",
        "slurk_id": "#4",
        "colour": "Green",
        "is_mat": False,
        "home_pos": {
            "x": 0.4860000014305115,
            "y": 1.0333631038665771,
            "z": 5.378699779510498,
        },
    },
    {
        "name": "Apple3",
        "slurk_id": "#5",
        "colour": "Yellow",
        "is_mat": False,
        "home_pos": {
            "x": 0.5040000081062317,
            "y": 1.0373632907867432,
            "z": 5.577000141143799,
        },
    },
    {
        "name": "Apple3Slice",
        "slurk_id": "#6",
        "colour": "Yellow",
        "is_mat": False,
        "home_pos": {
            "x": 0.5040000081062317,
            "y": 1.025663137435913,
            "z": 5.901700019836426,
        },
    },
    {
        "name": "Cup1",
        "slurk_id": "#7",
        "colour": "Green",
        "is_mat": False,
        "home_pos": {
            "x": 0.7879971265792847,
            "y": 1.0067720413208008,
            "z": 4.549003601074219,
        },
    },
    {
        "name": "Cup2",
        "slurk_id": "#8",
        "colour": "Orange",
        "is_mat": False,
        "home_pos": {
            "x": 0.8199986219406128,
            "y": 1.0067719221115112,
            "z": 4.806990623474121,
        },
    },
    {
        "name": "Bowl1",
        "slurk_id": "#9",
        "colour": "Black",
        "is_mat": False,
        "home_pos": {
            "x": 1.07542085647583,
            "y": 0.910454273223877,
            "z": 4.49299955368042,
        },
    },
    {
        "name": "Bowl2",
        "slurk_id": "#10",
        "colour": "Brown",
        "is_mat": False,
        "home_pos": {
            "x": 1.0049999952316284,
            "y": 0.8298299908638,
            "z": 4.761000156402588,
        },
    },
    {
        "name": "Bowl3",
        "slurk_id": "#11",
        "colour": "Grey",
        "is_mat": False,
        "home_pos": {
            "x": 0.9849997162818909,
            "y": 0.7876260280609131,
            "z": 5.063000202178955,
        },
    },
    {
        "name": "Bread1",
        "slurk_id": "#12",
        "colour": "White",
        "is_mat": False,
        "home_pos": {
            "x": 1.3809998035430908,
            "y": 0.9848300814628601,
            "z": 4.497000217437744,
        },
    },
    {
        "name": "Bread1Slice",
        "slurk_id": "#13",
        "colour": "White",
        "is_mat": False,
        "home_pos": {
            "x": 1.3694748878479004,
            "y": 1.14316987991333,
            "z": 4.797289848327637,
        },
    },
    {
        "name": "Bread2",
        "slurk_id": "#14",
        "colour": "Brown",
        "is_mat": False,
        "home_pos": {
            "x": 1.38100004196167,
            "y": 0.9848302006721497,
            "z": 5.063000202178955,
        },
    },
    {
        "name": "Bread2Slice",
        "slurk_id": "#15",
        "colour": "Brown",
        "is_mat": False,
        "home_pos": {
            "x": 1.3558368682861328,
            "y": 1.1330000162124634,
            "z": 5.32420015335083,
        },
    },
    {
        "name": "Egg1",
        "slurk_id": "#16",
        "colour": "Brown",
        "is_mat": False,
        "home_pos": {
            "x": 1.6330000162124634,
            "y": 0.9925320148468018,
            "z": 4.478000164031982,
        },
    },
    {
        "name": "Egg2",
        "slurk_id": "#17",
        "colour": "White",
        "is_mat": False,
        "home_pos": {
            "x": 1.6330000162124634,
            "y": 0.9925320148468018,
            "z": 4.630000114440918,
        },
    },
    {
        "name": "Pan1",
        "slurk_id": "#18",
        "colour": "Silver",
        "is_mat": False,
        "home_pos": {
            "x": 1.833000659942627,
            "y": 0.9288299083709717,
            "z": 4.549003601074219,
        },
    },
    {
        "name": "Pan2",
        "slurk_id": "#19",
        "colour": "Black",
        "is_mat": False,
        "home_pos": {
            "x": 1.8330004215240479,
            "y": 0.9288310408592224,
            "z": 4.799300193786621,
        },
    },
    {
        "name": "Plate1",
        "slurk_id": "#20",
        "colour": "White",
        "is_mat": False,
        "home_pos": {
            "x": 2.1510000228881836,
            "y": 1.0028302669525146,
            "z": 4.810999870300293,
        },
    },
    {
        "name": "Plate2",
        "slurk_id": "#21",
        "colour": "Blue",
        "is_mat": False,
        "home_pos": {
            "x": 2.1510000228881836,
            "y": 1.0028302669525146,
            "z": 4.585000038146973,
        },
    },
    {
        "name": "Vase1",
        "slurk_id": "#22",
        "colour": "Red",
        "is_mat": False,
        "home_pos": {
            "x": 2.3968935012817383,
            "y": 1.0388307571411133,
            "z": 4.544688701629639,
        },
    },
    {
        "name": "Vase2",
        "slurk_id": "#23",
        "colour": "Yellow",
        "is_mat": False,
        "home_pos": {
            "x": 2.400003433227539,
            "y": 1.038827896118164,
            "z": 4.734003067016602,
        },
    },
]


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

    def generate_thumbnails(self, blank_scene_controller):
        thumb_dir = os.path.join(blank_scene_controller.image_dir, "thumbnails")

        try:
            os.makedirs(thumb_dir)
        except FileExistsError:
            pass

        for asset in self.assets:
            name = asset["name"]
            blank_scene_controller.place_asset_at_location(name, 2, 1)
            img = blank_scene_controller.controller.last_event.cv2img
            cropped_img = img[425:625, 600:800]
            cv2.imwrite(os.path.join(thumb_dir, "{}.png".format(name)), cropped_img)
            blank_scene_controller.hide_asset(name)
        blank_scene_controller.stop()
