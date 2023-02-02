import hg
import functools
from libsmoother import Quarry
import clodius.tiles.format as hgfo
import numpy as np
import os
import json

BINS_PER_TILE = 256 # this seems to be a fixed value that cannot be changed
global quarry_by_path 
quarry_by_path = {}

def get_quarry(filepath: str):
    if filepath not in quarry_by_path:
        quarry_by_path[filepath] = Quarry(filepath)

        if quarry_by_path[filepath].get_value(["settings"]) is None:
            with open('default.json', 'r') as f:
                settings = json.load(f)
            quarry_by_path[filepath].set_value(["settings"], settings)

    return quarry_by_path[filepath]

def gen_resolutions(base_resolution, genome_size, f=2):
    ret = []
    x = 0
    while True:
        res = base_resolution * (f ** x)
        if res > genome_size:
            break
        ret.append(res)
        x += 1
    return ret

def resolutions_from_quarry(quarry):
    min_resolution = quarry.get_value(["dividend"])
    canvas_size_x, canvas_size_y = quarry.get_canvas_size()
    genome_size = max(canvas_size_x, canvas_size_y) * min_resolution
    return gen_resolutions(min_resolution, genome_size)

def tileset_info(filepath):
    """
    Get the tileset info

    Parameters:
    -----------

    filepath: str
        The location of the cooler file
    """
    quarry = get_quarry(filepath)
    min_resolution = quarry.get_value(["dividend"])
    canvas_size_x, canvas_size_y = quarry.get_canvas_size()

    return {
        "resolutions": tuple(resolutions_from_quarry(quarry)),
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
            ["AAA", canvas_size_x * min_resolution + 1]
        ]
    }

def make_tile(
    quarry,
    resolution,
    x_pos,
    y_pos
):
    """
    Generate tile for a given location.

    Parameters
    ---------
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
    # make sure settings are correct
    quarry.set_value(["settings", "interface", "fixed_number_of_bins"], True)
    quarry.set_value(["settings", "interface", "fixed_num_bins_x", "val"], BINS_PER_TILE)
    quarry.set_value(["settings", "interface", "fixed_num_bins_y", "val"], BINS_PER_TILE)

    min_resolution = quarry.get_value(["dividend"])
    # set current region
    tile_size = resolution * BINS_PER_TILE // min_resolution
    
    quarry.set_value(["area"], {
        "x_start": x_pos * tile_size,
        "x_end": (x_pos + 1) * tile_size,
        "y_start": y_pos * tile_size,
        "y_end": (y_pos + 1) * tile_size,
    })

    print("querying", resolution, x_pos, y_pos, quarry.get_value(["area"]))

    #quarry.update_cds()
    values = quarry.get_divided()
    size_x = quarry.get_axis_size(True)
    size_y = quarry.get_axis_size(False)

    out = np.ones((BINS_PER_TILE, BINS_PER_TILE), dtype=np.float32)
    for i in range(BINS_PER_TILE):
        for j in range(BINS_PER_TILE):
            idx = i * size_x + j
            out[i,j] = values[idx] if idx < len(values) else 0

    return out.ravel()



def tiles(filepath, tile_ids):
    """
    Generate tiles from a cooler file.
    Parameters
    ----------
    tileset: tilesets.models.Tileset object
        The tileset that the tile ids should be retrieved from
    tile_ids: [str,...]
        A list of tile_ids (e.g. xyx.0.0.1) identifying the tiles
        to be retrieved
    Returns
    -------
    generated_tiles: [(tile_id, tile_data),...]
        A list of tile_id, tile_data tuples
    """
    quarry = get_quarry(filepath)
    resolutions = resolutions_from_quarry(quarry)

    generated_tiles = []
    for tile_id in tile_ids:
        tile_id_parts = tile_id.split(".")
        tileset_id = tile_id_parts[0]
        zoom_level, x_pos, y_pos = list(map(int, tile_id_parts[1:4]))

        if zoom_level > len(resolutions):
                # this tile has too high of a zoom level specified
                continue
        resolution = resolutions[::-1][zoom_level]

        tile_data_by_position = make_tile(
            quarry,
            resolution,
            x_pos,
            y_pos
        )
        generated_tiles.append((tile_id, hgfo.format_dense_tile(tile_data_by_position)))
    return generated_tiles

@hg.tilesets.hash_absolute_filepath_as_default_uid
def smoother_impl(filepath: str, uid: str):
    return hg.tilesets.LocalTileset(
        datatype="matrix",
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        uid=uid,
    )

smoother = hg.server.register(smoother_impl)