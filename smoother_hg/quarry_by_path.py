from libsmoother import Quarry
from .synchronized import synchronized

global quarry_by_path 
quarry_by_path = {}

BINS_PER_TILE = 256 # this seems to be a fixed value that cannot be changed

def apply_necessary_hg_settings(quarry):
    quarry.print_callback = lambda s: None

    if quarry.get_value(["settings"]) is None:
        with open('default.json', 'r') as f:
            settings = json.load(f)
        quarry.set_value(["settings"], settings)

    quarry.set_value(["settings", "interface", "fixed_number_of_bins"], True)
    quarry.set_value(["settings", "filters", "incomplete_alignments"], True)
    quarry.set_value(["settings", "interface", "add_draw_area", "val"], 0)
    quarry.set_value(["settings", "filters", "cut_off_bin"], "cover_multiple")
    quarry.set_value(["settings", "interface", "fixed_num_bins_x", "val"], BINS_PER_TILE)
    quarry.set_value(["settings", "interface", "fixed_num_bins_y", "val"], BINS_PER_TILE)

def get_quarry_unsync(filepath: str):
    if filepath not in quarry_by_path:
        quarry_by_path[filepath] = Quarry(filepath)
        apply_necessary_hg_settings(quarry_by_path[filepath])

    return quarry_by_path[filepath]

@synchronized
def get_quarry(filepath: str):
    return get_quarry_unsync(filepath)