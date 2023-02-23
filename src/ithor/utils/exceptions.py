class DuplicateAssetError(Exception):
    pass


class MissingAssetError(Exception):
    pass


class GridCoordinateError(Exception):
    pass


class SlotFullError(Exception):
    pass


class NoObjectError(Exception):
    pass


class NoMatError(Exception):
    pass


class UnsupportedSystemError(Exception):
    pass


class MissingBuildFileError(Exception):
    pass


class ExistingThumbnailFolderError(Exception):
    pass


class MissingThumbnailsError(Exception):
    pass
