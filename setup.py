# pylint: skip-file
'''setup.py for arubatools'''
from setuptools import setup, find_packages

import versioneer


setup(
    name                 = 'mistifi',
    version              = versioneer.get_version(),
    cmdclass             = versioneer.get_cmdclass(),
    description          = 'Mist API Python module',
    long_description     = 'A Mist API client',
    author               = 'Primoz Marinsek',
    author_email         = 'primoz.marinsek@ocado.com',
    maintainer           = 'Primoz Marinsek',
    maintainer_email     = 'primoz.marinsek@ocado.com',
    packages             = find_packages(),
    include_package_data = True,
    install_requires     = [
        'requests',
        'logzero',
    ],
    tests_require        = [
        'requests',
        'responses',
        'logzero',
    ],
)
