import os
import platform

from ithor.utils.exceptions import MissingBuildFileError, UnsupportedSystemError


def get_local_build_path():
    """
    Checks the system in use and ensures appropriate local build files are present.

    Raises
    ------
    MissingBuildFileError
        Raises MissingBuildFileError if the system is Linux or MacOS but the build files are missing.
    UnsupportedSystemError
        Raises UnsupportedSystemError if the system is Windows or unrecognised.

    Returns
    -------
    string
        The filepath for the appropriate local build files.

    """
    system = platform.system()
    if system == "Darwin":
        if not os.path.exists("builds/thor-OSXIntel64-local/thor-OSXIntel64-local"):
            raise MissingBuildFileError(
                "You do not have the local build files for MacOS, please download them and put them in the builds directory."
            )
        else:
            return "thor-OSXIntel64-local"
    elif system == "Linux":
        if not os.path.exists("builds/thor-Linux64-local/thor-Linux64-local"):
            raise MissingBuildFileError(
                "You do not have the local build files for Linux, please download them and put them in the builds directory."
            )
        else:
            return "builds/thor-Linux64-local/thor-Linux64-local"
    elif system == "Windows":
        raise UnsupportedSystemError(
            "Windows is not supported by iTHOR, please use Linux or MacOS."
        )
    else:
        raise UnsupportedSystemError(
            "The system you are using is unrecognised, please use Linux or MacOS."
        )
