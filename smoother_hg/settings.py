import ipywidgets
from .quarry_by_path import get_quarry
from .synchronized import synchronized
from typing import Any, List
from higlass_widget.widget import HiGlassWidget
from hg.api import View

@synchronized
def update_setting(filepath: str, widget: HiGlassWidget, view: View, setting: List[str], value: Any):
    get_quarry(filepath).set_value(setting, value)
    widget.reload(view.uid)



def default_gui(filepath: str, widget: HiGlassWidget, view: View):
    def update_setting_local(setting, value):
        update_setting(filepath, widget, view, setting, value)

    def map_q_val_change(change):
        update_setting_local(["settings", "filters", "mapping_q", "val_min"], change['new'])
        
    def normalization_val_change(change):
        key = ["settings", "normalization", "normalize_by"]
        if change["new"] == 2:
            update_setting_local(key, "hi-c")
        elif change["new"] == 1:
            update_setting_local(key, "dont")
        
    def ddd_val_change(change):
        update_setting_local(["settings", "normalization", "normalize_by", "ddd"], change['new'])

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