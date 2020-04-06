# pylint: skip-file
'''setup.py for arubatools'''
from setuptools import setup, find_packages

import versioneer
import pathlib

# The directory containing the README.md file
HERE = pathlib.Path(__file__).parent
# The contents of the README.md file
README = (HERE / "README.md").read_text()

setup(
    name                 = 'mistifi',
    version              = versioneer.get_version(),
    cmdclass             = versioneer.get_cmdclass(),
    description          = 'Mist API Python module',
    long_description     = README,
    long_description_content_type ="text/markdown",
    author               = 'Primoz Marinsek',
    author_email         = 'primoz.marinsek@ocado.com',
    license              = "Apache-2.0",
    packages             = find_packages(),
    include_package_data = True,
    install_requires     = [
        'requests',
        'logzero',
    ],
    tests_require        = [
        'responses',
        'pytest',
    ],
)
