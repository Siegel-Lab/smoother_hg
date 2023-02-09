from distutils.core import setup

VERSION = "0.1.0"

setup(
    name="smoother_hg",
    version=VERSION,
    author='Markus Schmidt',
    author_email='markus.rainer.schmidt@gmail.com',
    license='MIT',
    url='https://github.com/Siegel-Lab/smoother_hg',
    description="integration of hg and libsmoother",
    long_description="",
    packages=["smoother_hg"],
    extras_require={"test": "pytest"},
    data_files=[("data", ["data/default.json"])],
    zip_safe=False,
    python_requires=">=3.5",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'libsmoother @ git+https://github.com/Siegel-Lab/libSmoother@stable-latest',
        'hg @ git+https://github.com/manzt/hg.git@77986811fb7103fde1da97058c2e407989b4f31c',
        "ipywidgets==7.7.2", # @todo for some reason only exactly this version works for me :(
        "clodius>=0.19.0",
    ]
)