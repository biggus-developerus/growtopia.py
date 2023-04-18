import os

from setuptools import find_packages, setup

packages = [
    os.path.join(root).replace("\\", ".")
    for root, _, files in os.walk("growtopia")
    if "__init__.py" in files
]

setup(
    packages=find_packages(include=packages)
)
