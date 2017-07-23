from setuptools import find_packages, setup
from slyrics.version import __version__

setup(
    name="slyrics",
    version=__version__,
    description="An external lyrics addon for Spotify",
    author="Alexander Bakker",
    author_email="github@alexbakker.me",
    url="https://github.com/Impyy/slyrics",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "slyrics=slyrics:main",
        ],
    },
    license="GPLv3"
)
