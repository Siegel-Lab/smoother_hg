import clodius.tiles.format as hgfo
import numpy as np

MAX_ITER = 80
def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1
    return n

RESOLUTIONS = [10**n for n in range(1, 10)]
MAX_DATA_SIZE = 10**11
BINS_PER_TILE = 256 # this seems to be a fixed value that cannot be changed

def make_tile(
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

    tile_size = resolution * BINS_PER_TILE / MAX_DATA_SIZE

    out = np.ones((BINS_PER_TILE, BINS_PER_TILE), dtype=np.float32)
    for i in range(BINS_PER_TILE):
        for j in range(BINS_PER_TILE):
            out[i,j] = mandelbrot(complex((i / BINS_PER_TILE + y_pos) * tile_size, 
                                            (j / BINS_PER_TILE + x_pos) * tile_size))

    return out.ravel()


def tileset_info(filepath):
    """
    Get the tileset info

    Parameters:
    -----------

    filepath: str
        The location of the cooler file
    """
    return {
        "resolutions": tuple(RESOLUTIONS),
        'transforms': [], 
        'max_pos': [
            MAX_DATA_SIZE,
            MAX_DATA_SIZE
        ], 
        'min_pos': [
            1,
            1
        ],
        'chromsizes': [
            ["AAA", MAX_DATA_SIZE]
        ]
    }



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
    generated_tiles = []
    for tile_id in tile_ids:
        tile_id_parts = tile_id.split(".")
        tileset_id = tile_id_parts[0]
        zoom_level, x_pos, y_pos = list(map(int, tile_id_parts[1:4]))

        if zoom_level > len(RESOLUTIONS):
                # this tile has too high of a zoom level specified
                continue
        resolution = RESOLUTIONS[::-1][zoom_level]

        tile_data_by_position = make_tile(
            resolution,
            x_pos,
            y_pos
        )
        generated_tiles.append((tile_id, hgfo.format_dense_tile(tile_data_by_position)))
    return generated_tiles

