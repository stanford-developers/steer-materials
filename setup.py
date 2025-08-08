from distutils.core import setup
from setuptools import find_packages
import pathlib
import re

root = pathlib.Path(__file__).parent
init = root / "steer_materials" / "__init__.py"
version = re.search(r'__version__\s*=\s*"([^"]+)"', init.read_text()).group(1)

setup(
    name='steer-materials',
    version=version, 
    description='Modelling energy storage from cell to site - STEER OpenCell Design',
    author='Nicholas Siemons',
    author_email='nsiemons@stanford.edu',
    url="https://github.com/nicholas9182/steer-materials/",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "datetime",
        "scipy",
        "shapely",
        "plotly",
        "dash",
        "dash_bootstrap_components",
        "flask_caching",
        "nbformat",
        "scipy"
    ],
    scripts=[],
    classifiers=[ 
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)


