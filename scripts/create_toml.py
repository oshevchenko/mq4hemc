import subprocess
import toml

# Get the latest tag from git
tag = subprocess.getoutput('git describe --abbrev=4 --dirty --always')

# Load the pyproject.toml file
with open('pyproject.toml.in', 'r') as file:
    pyproject = toml.load(file)

# Update the version
pyproject['tool']['poetry']['version'] = tag

# Write the pyproject.toml file
with open('pyproject.toml', 'w') as file:
    toml.dump(pyproject, file)
