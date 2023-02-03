from libsmoother import Quarry
import logging

"""
higlass tiles are always 256x256 pixels
"""
BINS_PER_TILE = 256

def __apply_necessary_hg_settings(quarry: Quarry):
    """
    Modifies the session variables in a Quarry so that it can be displayed in higlass.
    This includes for example only rendering exactly the requested area 
    or rendering with a fixed number of bins for the x and the y axis.
    """
    # prevent libsmoother from spamming jupyter-notebook with prints but log the output instead
    logger = logging.getLogger(__name__) # @todo this does not work yet
    quarry.print_callback = lambda s: logger.info(s)

    # if settings is empty store the default settings there
    if quarry.get_value(["settings"]) is None:
        with open('default.json', 'r') as f:
            settings = json.load(f)
        quarry.set_value(["settings"], settings)

    # @todo probably some other settings are required to be a certain way for hg

    # render exactly the given number of bins
    quarry.set_value(["settings", "interface", "fixed_number_of_bins"], True)

    # give the number of bins to render on the x axis
    quarry.set_value(["settings", "interface", "fixed_num_bins_x", "val"], BINS_PER_TILE)

    # give the number of bins to render on the y axis
    quarry.set_value(["settings", "interface", "fixed_num_bins_y", "val"], BINS_PER_TILE)

    # set the additional draw area to zero
    # in smoother we want to draw an area a little larger than the visible area
    # in hg, with the tiles system we want to render exact
    quarry.set_value(["settings", "interface", "add_draw_area", "val"], 0)

    # make sure that no bin is skipped because it is overlapping with the end of a contig
    # smoother can adapt the coordinate system to deal with smaller bins but for hg we just force an even size
    quarry.set_value(["settings", "filters", "cut_off_bin"], "cover_multiple")


    # do not filter out incomplete alignments by default (this is not strictly necessary)
    quarry.set_value(["settings", "filters", "incomplete_alignments"], True)

"""
Global dictionary to cache the loaded libSmoother.Quarry objects
"""
global __quarry_by_path
__quarry_by_path = {}


def get_quarry(filepath: str):
    """
    Get a cached or load a new libsmoother.Quarry object.
    If this filepath has not been opened yet a new quarry ise created and then cached.
    If the path has been opened before the cached object is returned.

    This function is not synchronized.

    Parameters
    ----------
    filepath: str
        the path to the smoother index which is also used as an ID for that idexes Quarry object.

    Returns
    -------
    A libsmoother.Quarry object.
    """
    if filepath not in __quarry_by_path:
        __quarry_by_path[filepath] = Quarry(filepath)
        __apply_necessary_hg_settings(__quarry_by_path[filepath])

    return __quarry_by_path[filepath]


def del_quarry(filepath: str):
    """
    Delete a libsmoother.Quarry object from the cache.
    This function is not synchronized.
    """
    del __quarry_by_path[filepath]