## TEST 1

import hg
import smoother_hg

PATH = "../smoother_out/radicl.smoother_index"

smoother_hg.smoother(PATH)




## TEST 2
import libsmoother
import json

q = libsmoother.Quarry(PATH)


if q.get_value(["settings"]) is None:
    with open('smoother_hg/default.json', 'r') as f:
        settings = json.load(f)
    q.set_value(["settings"], settings)

q.update_cds()

del q





## TEST 3

tileset = smoother_hg.smoother(PATH)
track = tileset.track("heatmap")
view = hg.view(track)
interface = smoother_hg.widgets(tileset, view)


view.display()
interface