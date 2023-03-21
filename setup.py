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
    Extension(
        "growtopia.extensions.parse",
        ["growtopia/extensions/parse.pyx"],
    ),
]

cythonize(extensions, language_level="3")

for ext in extensions:
    for src in ext.sources:
        if src.endswith(".pyx"):
            ext.sources.remove(src)
            ext.sources.append(src[:-3] + "c")

setup(
    packages=find_packages(include=packages),
    ext_modules=extensions,
    include_package_data=True,
    package_data=package_data,
)
