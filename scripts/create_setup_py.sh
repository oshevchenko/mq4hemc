#!/bin/bash
echo -n "__version__ = version = '" > ${S}/src/mq4hemc/_version.py
(cd ${S} && echo -n $(git describe --abbrev=4 --always) | sed 's/-/.dev/g' | sed 's/.devg/+g/g' >> ./src/mq4hemc/_version.py)
echo "'" >> ${S}/src/mq4hemc/_version.py
cat > ${S}/setup.py <<-EOF
import io
import os
import re
version="${PV}"
version_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/mq4hemc/_version.py'))
if os.path.isfile(version_file):
    with io.open(version_file, "rt", encoding="utf8") as f:
        match = re.search(r"__version__ = version = '(.*)'", f.read())
        if match:
            version = match.group(1)

from setuptools import setup
setup(
    version=version,
)
EOF

