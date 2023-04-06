import hg
import functools
import clodius.tiles.format as hgfo
import numpy as np
import os
import json
from .quarry_by_path import get_quarry, BINS_PER_TILE
from .synchronized import synchronized
from libsmoother import Quarry
from typing import List


def __gen_resolutions(base_resolution: int, genome_size: int, f: int=2):
    """
    Computes a set of resolutions: { r | r = base_resolution * f ^ x, r <= genome_size, x \in N_0 }
    """
    ret = []
    x = 0
    while True:
        res = base_resolution * (f ** x)
        if res > genome_size:
            break
        ret.append(res)
        x += 1
    return ret

def __resolutions_from_quarry(quarry: Quarry):
    """
    Takes a libSmoother.Quarry object and returns a set of resolutions that can be deplayed by the object
    """
    min_resolution = quarry.get_value(["dividend"])
    canvas_size_x, canvas_size_y = quarry.get_canvas_size(lambda s: None)
    genome_size = max(canvas_size_x, canvas_size_y) * min_resolution
    return __gen_resolutions(min_resolution, genome_size)

@synchronized
def tileset_info(filepath: str):
    """
    Get the tileset info

    Parameters
    ----------
    filepath: str
        the path to the smoother index which is also used as an ID for that idexes Quarry object.

    Returns
    -------
    A dictionary containing information about the tilset, as e.g. the number of available resolutions.
    """
    quarry = get_quarry(filepath)
    min_resolution = quarry.get_value(["dividend"])

    # get canvas size (which is given as a factor of the minimal resolution)
    canvas_size_x, canvas_size_y = quarry.get_canvas_size(lambda s: None)

    return {
        "resolutions": tuple(__resolutions_from_quarry(quarry)),
        'transforms': [], 
        'max_pos': [
            canvas_size_x * min_resolution + 1,
            canvas_size_y * min_resolution + 1
        ], 
        'min_pos': [
            1,
            1
        ],
        'chromsizes': [
            ["AAA", canvas_size_x * min_resolution + 1] # @todo where is this info used and do i need to provide it?
        ],
        "mirror_tiles": "false"
    }


def __make_tile(
    quarry: Quarry,
    resolution: int,
    x_pos: int,
    y_pos: int
):
    """
    Generate tile for a given location.

    Parameters
    ----------
    quarry: Quarry
        libsmoother.Quarry object that holds a smoother-index and an associated rendering session. i.e. all information needed for redering the tile.
    resolution: int
        the resolution of the tile
    x_pos: int
        The starting x position
    y_pos: int
        The starting y position

    Returns
    -------
    data_by_tilepos: {(x_pos, y_pos) : np.array}
        A dictionary of tile data indexed by tile positions
    """
    # set region to be rendered
    min_resolution = quarry.get_value(["dividend"])
    tile_size = resolution * BINS_PER_TILE // min_resolution
    quarry.set_value(["area"], {
        "x_start": x_pos * tile_size - 1,
        "x_end": (x_pos + 1) * tile_size - 1,
        "y_start": y_pos * tile_size - 1,
        "y_end": (y_pos + 1) * tile_size - 1,
    })

    # quarry data from libSmoother
    values = quarry.get_combined(lambda s: None)
    size_x = quarry.get_axis_size(True, lambda s: None)
    size_y = quarry.get_axis_size(False, lambda s: None)

    # @todo this can be done better
    out = np.ones((BINS_PER_TILE, BINS_PER_TILE), dtype=np.float32)
    for i in range(BINS_PER_TILE):
        for j in range(BINS_PER_TILE):
            idx = j * size_y + i
            out[i,j] = values[idx] if i < size_y and j < size_x else 0

    return out.ravel()


@synchronized
def tiles(filepath: str, tile_ids: List[str]):
    """
    Generate tiles from a smoother index.


    Details
    -------

    At the moment this function (as well as) all functions that use a libsmoother.Quarry object are synchronize
    (i.e. there is a mutex that ensures that at a time only a single of these functions is running).
    This is necessary since libSmoother.Quarry uses a .json object for its configuration.
    This json object contains settings like the slider values as well as the area that shall be rendered.
    Redering a region using this object and changing parameters creates a race condition...
    @todo This issue can be resolved by adding 'sessions' to the Quarry object: 
        - inside a session local variables as e.g. the area to be rendered can be set

    Parameters
    ----------
    filepath: 
        the path to the smoother index which is also used as an ID for that idexes Quarry object.
    tile_ids: [str,...]
        A list of tile_ids (e.g. xyx.0.0.1) identifying the tiles
        to be retrieved

    Returns
    -------
    generated_tiles: [(tile_id, tile_data),...]
        A list of tile_id, tile_data tuples
    """
    # get or load the quarry
    quarry = get_quarry(filepath)
    resolutions = __resolutions_from_quarry(quarry)

    generated_tiles = []
    # iterate over all tiles
    for tile_id in tile_ids:
        # extract zoom_level, x_pos, y_pos from the tile_id
        tile_id_parts = tile_id.split(".")
        tileset_id = tile_id_parts[0]
        zoom_level, x_pos, y_pos = list(map(int, tile_id_parts[1:4]))

        # determine the requested resolution
        if zoom_level > len(resolutions):
            # this tile has too high of a zoom level specified
            continue
        resolution = resolutions[::-1][zoom_level]

        # query the tile
        tile_data_by_position = __make_tile(
            quarry,
            resolution,
            x_pos,
            y_pos
        )

        # store the tile in a compressed format
        generated_tiles.append((tile_id, hgfo.format_dense_tile(tile_data_by_position)))
    return generated_tiles



@hg.tilesets.hash_absolute_filepath_as_default_uid
def __smoother_tileset_factory(filepath: str, uid: str):
    """
    Factory function for the local smoother tileset
    """
    return hg.tilesets.LocalTileset(
        datatype="matrix",
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        uid=uid,
    )


"""
register the smoother tileset
"""
smoother = hg.server.register(__smoother_tileset_factory)