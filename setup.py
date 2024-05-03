from setuptools import setup
import subprocess
tag = subprocess.getoutput('git describe --abbrev=4 --dirty --always')

setup(
    version=tag
)
