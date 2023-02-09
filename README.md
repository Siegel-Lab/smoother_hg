# smoother_hg - Integrates hg and Smoother

This package allows opening smoother indices in HiGlass.

- [Smoother's GitHub](https://github.com/Siegel-Lab/Smoother "go to smoother's github") 
- [hg's GitHub](https://github.com/manzt/hg "go to hg's github") 

## Quickstart: 

prerequisites:
- conda should be installed
- build-essential should be installed

\
create & activate a new conda environment (optional)
```
conda create -y -n smoother_hg python=3.8
conda activate smoother_hg
```

install the proper compilers
```
conda install -y gcc=9.4.0 gxx=9.4.0 -c conda-forge
```

Install smoother_hg (and all requirements) from GitHub.
```
git clone https://github.com/Siegel-Lab/smoother_hg.git
cd smoother_hg
git checkout stable-latest
pip install -e . --no-binary libsps,libsmoother

# hg only works with numpy<=1.23.0 but does not declare this
pip install numpy==1.23.0
```

Download 2 example smoother indices.
```
wget https://syncandshare.lrz.de/dl/fiFPBw32Rc3cJs1qfsYkKa/radicl.smoother_index.zip
wget https://syncandshare.lrz.de/dl/fi8q6iroKx49azsZLHxeYB/micro-c.smoother_index.zip

conda install -y unzip
unzip radicl.smoother_index.zip
unzip micro-c.smoother_index.zip
```

Then open Example.ipynb in jupyter-lab or -notebook.
