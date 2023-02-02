import ipywidgets
from .quarry_by_path import get_quarry_unsync
from .synchronized import synchronized

@synchronized
def update_setting(filepath, setting, value):
    get_quarry_unsync(filepath).set_value(setting, value)
    # @todo update should be replaced with a better way to rerender the server...
    view.update()

def widgets(filepath, view):
    def map_q_val_change(change):
        update_setting(["settings", "filters", "mapping_q", "val_min"], change['new'])
        
    def normalization_val_change(change):
        key = ["settings", "normalization", "normalize_by"]
        if change["new"] == 2:
            update_setting(key, "hi-c")
        elif change["new"] == 1:
            update_setting(key, "dont")
        
    def ddd_val_change(change):
        update_setting(["settings", "normalization", "normalize_by", "ddd"], change['new'])

    mapping_quality = ipywidgets.IntSlider(max=256, continuous_update=False)
    mapping_quality.observe(map_q_val_change, names='value')
    mapping_quality_box = ipywidgets.HBox([ipywidgets.Label("Mapping Quality Minimum"), mapping_quality])

    normalization = ipywidgets.Dropdown(
        options=[('None', 1), ('Iterative Correction', 2)],
        value=1,
    )
    normalization.observe(normalization_val_change, names='value')
    normalization_box = ipywidgets.HBox([ipywidgets.Label("Normalization"), normalization])

    ddd = ipywidgets.Checkbox(
        value=False,
        description='Remove Distance Dependant Decay',
        disabled=False,
        indent=False
    )
    ddd.observe(ddd_val_change, names='value')

    return ipywidgets.VBox([mapping_quality_box, normalization_box, ddd])