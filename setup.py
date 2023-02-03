from distutils.core import setup

# @todo move into smoother

setup(
    name="smoother_hg",
    version="0.1.0",
    author='Markus Schmidt',
    author_email='markus.rainer.schmidt@gmail.com',
    license='MIT',
    url='https://github.com/MarkusRainerSchmidt/smoother_hg',
    description="integration of hg and libsmoother",
    long_description="",
    packages=["smoother_hg"],
    extras_require={"test": "pytest"},
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
        'libsmoother', # @todo turn into git+https://github.com/bla/bla/bla
        'hg', # @todo turn into git+https://github.com/bla/bla/bla
    ]
)