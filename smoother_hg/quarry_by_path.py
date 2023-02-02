from libsmoother import Quarry
from .synchronized import synchronized

global quarry_by_path 
quarry_by_path = {}

def get_quarry_unsync(filepath: str):
    if filepath not in quarry_by_path:
        quarry_by_path[filepath] = Quarry(filepath)
        quarry_by_path[filepath].print_callback = lambda s: None

        if quarry_by_path[filepath].get_value(["settings"]) is None:
            with open('default.json', 'r') as f:
                settings = json.load(f)
            quarry_by_path[filepath].set_value(["settings"], settings)

    return quarry_by_path[filepath]

@synchronized
def get_quarry(filepath: str):
    return get_quarry_unsync(filepath)