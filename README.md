# smoother_hg - Integrates hg and Smoother

This package allows opening smoother indices in HiGlass.

## Quickstart: 

create & activate a new environment (optional)
```
conda create -y -n smoother_hg python=3.8
conda activate smoother_hg
```

Install smoother_hg (and all requirements) from GitHub.
```
git clone https://github.com/Siegel-Lab/smoother_hg.git
cd smoother_hg
pip install -e .
```

Download 2 example smoother indices.
```
wget https://syncandshare.lrz.de/dl/fiFPBw32Rc3cJs1qfsYkKa/radicl.smoother_index.zip

conda install unzip
unzip radicl.smoother_index.zip
```

Then open Example.ipynb in jupyter-lab or -notebook.
