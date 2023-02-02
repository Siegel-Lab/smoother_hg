import hg
import smoother_hg

path = "../../smoother_out/radicl.smoother_index"
tileset = smoother_hg.smoother(path)
track = tileset.track("heatmap")
view = hg.view(track)
interface = smoother_hg.widgets(path, view)

view.widget()