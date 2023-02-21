from src.ithor.utils.exceptions import DuplicateAssetError
from src.ithor.utils.exceptions import MissingAssetError
import os
import cv2

assets = [
    {
        "name": "Square1",
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
            blank_scene_controller.place_asset(name, 2, 1)
            img = blank_scene_controller.controller.last_event.cv2img
            cropped_img = img[425:625, 600:800]
            cv2.imwrite(os.path.join(thumb_dir, "{}.png".format(name)), cropped_img)
            blank_scene_controller.hide_asset(name)
        blank_scene_controller.stop()
