import ipywidgets

def widgets(tileset, view):
    def map_q_val_change(change):
        print(change)
        view.update()
        
    def normalization_val_change(change):
        print(change)
        view.update()
        
    def ddd_val_change(change):
        print(change)
        view.update()

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