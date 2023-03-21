import os

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

packages = [
    os.path.join(root).replace("\\", ".")
    for root, _, files in os.walk("growtopia")
    if "__init__.py" in files
]

package_data = {
    os.path.join(root).replace("\\", "."): [file]
    for root, _, files in os.walk("growtopia")
    for file in files
    if file.endswith(".pyi")
}

extensions = [
    Extension("growtopia.extensions.parse", ["growtopia/extensions/parse.pyx"]),
]

setup(
    name="growtopia.py",
    packages=find_packages(include=packages),
    ext_modules=cythonize(extensions, language_level="3"),
    package_data=package_data,
)
